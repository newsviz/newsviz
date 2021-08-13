# Copyright © 2021 @vtrokhymenko. All rights reserved.
# Copyright © 2020, 2021 Sviatoslav Kovalev. All rights reserved.
# Copyright © 2020 Artem Tuisuzov. All rights reserved.
#    This file is part of NewsViz Project.
#
#    NewsViz Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NewsViz Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NewsViz Project.  If not, see <https://www.gnu.org/licenses/>.
import configparser
import json
import logging
import multiprocessing as mp
import os

import joblib
import luigi
import numpy as np
import pandas as pd
import topic_model
import tqdm
from preprocessing_tools import Preprocessing

logger = logging.getLogger("luigi-interface")


def get_dirs(path):
    dirpaths = []
    for item in os.listdir(path):
        print(item)
        if os.path.isdir(os.path.join(path, item)):
            dirpaths.append(item)
    return dirpaths


def get_fnames(path):
    fnames = []
    for item in os.listdir(path):
        if os.path.isdir(item) or not item.endswith(".csv.gz"):
            continue
        fnames.append(item)
    return fnames


def make_path_pairs(input_path, output_path):
    path_pairs = []
    for dirname in get_dirs(input_path):
        for fname in get_fnames(os.path.join(input_path, dirname)):
            readpath = os.path.join(input_path, dirname, fname)
            writepath = os.path.join(output_path, dirname, fname)
            path_pairs.append((readpath, writepath))
    return path_pairs


MULTIPROCESSING = True
CPU_COUNT = mp.cpu_count()


def apply_function_mp(function, series, chunksize=None):
    if MULTIPROCESSING:
        chunksize = chunksize or (len(series) // CPU_COUNT // 2)
        with mp.Pool(CPU_COUNT, maxtasksperchild=1) as pool:
            return list(
                tqdm.tqdm(
                    pool.imap(function, series, chunksize=chunksize),
                    # pool.imap(partial(function, language=language), series),
                    total=len(series),
                )
            )

    return series.apply(function)


class PreprocessorTask(luigi.Task):
    """expects directory with csv files in it
    files must contain columns: text, topics, date
    """

    conf = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super(PreprocessorTask, self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.config.read(self.conf)
        self.input_path = self.config["common"]["raw_path"]
        self.output_path = self.config["preprocessor"]["output_path"]
        self.path_pairs = make_path_pairs(self.input_path, self.output_path)
        self.language = self.config["preprocessor"]["language"]

        # For MacOS and Python 3.8
        # mp.set_start_method("fork")

    def run(self):
        logger = logging.getLogger("luigi-interface")
        for readpath, writepath in self.path_pairs:
            dname = os.path.dirname(writepath)
            os.makedirs(dname, exist_ok=True)

            logger.info("process %s", readpath)
            data = pd.read_csv(readpath, compression="gzip")

            preprocess = Preprocessing(language=self.language)

            logger.info("process %s, clean text", readpath)
            data["cleaned_text"] = apply_function_mp(preprocess.clean_text, data["text"])

            logger.info("process %s, lemmatize", readpath)
            data["lemmatized"] = apply_function_mp(preprocess.lemmatize, data["cleaned_text"], chunksize=1000)

            logger.info("process %s, create ids", readpath)
            data["row_id"] = np.arange(data.shape[0])
            logger.info("write to %s", writepath)
            data[["row_id", "date", "topics", "lemmatized"]].to_csv(writepath, index=False, compression="gzip")

    def output(self):
        outputs = []
        for readpath, writepath in self.path_pairs:
            outputs.append(luigi.LocalTarget(writepath))
        return outputs


class RubricClassifierTask(luigi.Task):
    """depends on previous step
    and requires pretrained classifier with method predict()
    and features extractor with method transform()
    """

    conf = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super(RubricClassifierTask, self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.config.read(self.conf)
        self.input_path = self.config["preprocessor"]["output_path"]
        self.output_path = self.config["classifier"]["output_path"]
        self.path_pairs = make_path_pairs(self.input_path, self.output_path)
        self.classifier_path = self.config["classifier"]["classifier_path"]
        self.ftransformer_path = self.config["classifier"]["ftransformer_path"]

    def requires(self):
        return PreprocessorTask(conf=self.conf)

    def run(self):
        logger.info("start %s task", self.__class__.__name__)

        model = joblib.load(self.classifier_path)
        feats_trnsfr = joblib.load(self.ftransformer_path)

        for readpath, writepath in self.path_pairs:
            os.makedirs(os.path.dirname(writepath), exist_ok=True)
            logger.info("process %s", readpath)
            data = pd.read_csv(readpath, compression="gzip")
            data.dropna(inplace=True, subset=["lemmatized"])
            feats = feats_trnsfr.transform(data["lemmatized"].values)
            preds = model.predict(feats)
            data["rubric_preds"] = preds
            data[["row_id", "date", "rubric_preds"]].to_csv(writepath, index=False, compression="gzip")

    def output(self):
        outputs = []
        for readpath, writepath in self.path_pairs:
            outputs.append(luigi.LocalTarget(writepath))
        return outputs


class TopicPredictorTask(luigi.Task):
    """depends on previous step
    requires pretrained topic models for each class
    """

    # TODO: save top words
    conf = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super(TopicPredictorTask, self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.config.read(self.conf)
        self.input_path_c = self.config["classifier"]["output_path"]
        self.input_path_l = self.config["preprocessor"]["output_path"]
        self.output_path = self.config["topic"]["output_path"]
        self.model_path = self.config["topic"]["model_path"]
        self.viz_path = self.config["visualizer"]["data_path"]
        clf_path = self.config["classifier"]["classifier_path"]
        # TODO: add class to classname mapping
        class_names = self.config["classifier"]["class_names"]
        # TODO: move model params to the model wrapper script
        self.dict_path = self.config["topic"]["dict_path"]

        # self.fnames = get_fnames(self.input_path_c)
        self.path_pairs = make_path_pairs(self.input_path_c, self.input_path_l)

        self.class_renamer = json.load(open(os.path.join(os.path.dirname(clf_path), class_names), "r"))

    def requires(self):
        return RubricClassifierTask(conf=self.conf)

    def make_writepath(self, source_name, cl):
        fname = "{}.csv.gz".format(self.class_renamer[str(cl)])
        dst = os.path.join(self.viz_path, source_name)
        if not os.path.exists(dst):
            os.makedirs(dst)
        return os.path.join(dst, fname)

    def run_model(self, source_name, cl, data):
        # Init model
        tm = topic_model.TopicModelWrapperARTM(self.output_path, source_name + "_" + str(cl))

        # TODO: add option to replace class label by class name
        writepath = self.make_writepath(source_name, cl)
        os.makedirs(os.path.dirname(writepath), exist_ok=True)

        # Load model with dictionary
        tm.load_model(
            os.path.join(self.model_path.format(cl)),
            os.path.join(self.dict_path.format(cl)),
        )

        # Prepare data for transformation
        tm.prepare_data(data["lemmatized"].values)

        # Get predictions and join them to dates
        # TODO: check if indexing is right after this crazy trick
        theta = tm.transform()
        result = theta.merge(
            data[["date"]],
            left_index=True,
            right_index=True,
        )

        # save top words for visualizer
        tm.save_top_words(os.path.join(self.viz_path, f"tw_{self.class_renamer[str(cl)]}.json"))
        result.to_csv(writepath, compression="gzip", index=False)

    def run(self):
        os.makedirs(os.path.join(self.output_path, "topwords"), exist_ok=True)
        for readpath_c, readpath_l in self.path_pairs:
            data_c = pd.read_csv(readpath_c, compression="gzip")
            data_l = pd.read_csv(readpath_l, compression="gzip")
            data = data_l.merge(data_c[["row_id", "rubric_preds"]], on="row_id", how="inner")
            classes = data["rubric_preds"].unique()
            source_name = os.path.dirname(readpath_c).split("/")[-1]
            for cl in classes:
                mask = data["rubric_preds"] == cl
                self.run_model(source_name, cl, data[mask].copy().reset_index())
                # -----------
                tm = topic_model.TopicModelWrapperARTM(self.output_path, source_name + "_" + str(cl))  # noqa:

    def output(self):
        # TODO: add comments with example
        outputs = []
        for readpath_c, readpath_l in self.path_pairs:
            data_c = pd.read_csv(readpath_c, compression="gzip")
            classes = data_c["rubric_preds"].unique()
            for cl in classes:
                source_name = os.path.dirname(readpath_c).split("/")[-1]
                writepath = self.make_writepath(source_name, cl)
                outputs.append(luigi.LocalTarget(writepath))
        return outputs
