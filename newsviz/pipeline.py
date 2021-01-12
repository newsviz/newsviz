# Copyright © 2020 Sviatoslav Kovalev. All rights reserved.
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
import datetime
import json
import logging
import multiprocessing as mp
import os
import sys

import joblib
import luigi
import numpy as np
import pandas as pd
import topic_model
import tqdm
from luigi.contrib import sqla
from preprocessing_tools import clean_text, lemmatize
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("./database")
import uuid

from models import News

logger = logging.getLogger("luigi-interface")


def get_fnames(path):
    fnames = []
    for item in os.listdir(path):
        if os.path.isdir(item) or not item.endswith(".csv.gz"):
            continue
        fnames.append(item)
    return fnames


MULTIPROCESSING = True
CPU_COUNT = max(mp.cpu_count() - 4, 1)


def apply_function_mp(function, series):
    if MULTIPROCESSING:
        with mp.Pool(CPU_COUNT) as pool:
            return list(
                tqdm.tqdm(
                    pool.imap(function, series),
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
        self.fnames = get_fnames(self.input_path)

    def run(self):
        logger = logging.getLogger("luigi-interface")
        for fname in self.fnames:
            logger.info("process %s", fname)
            readpath = os.path.join(self.input_path, fname)
            writepath = os.path.join(self.output_path, fname)
            data = pd.read_csv(readpath, compression="gzip")

            logger.info("process %s, clean text", fname)
            data["cleaned_text"] = apply_function_mp(clean_text, data["text"])

            logger.info("process %s, lemmatize", fname)
            data["lemmatized"] = apply_function_mp(
                lemmatize,
                data["cleaned_text"],
            )

            logger.info("process %s, create ids", fname)
            data["row_id"] = np.arange(data.shape[0])
            logger.info("write to %s", writepath)
            data[["row_id", "date", "topics", "lemmatized"]].to_csv(writepath, index=False, compression="gzip")

    def output(self):
        outputs = []
        for fname in self.fnames:
            writepath = os.path.join(self.output_path, fname)
            outputs.append(luigi.LocalTarget(writepath))
        return outputs


class DBTransfer(luigi.Task):

    conf = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super(DBTransfer, self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.config.read(self.conf)
        self.input_path = self.config["database"]["input_path"]
        print("=" * 100)
        print(self.input_path)
        print("=" * 100)
        self.database = self.config["database"]["database"]
        self.engine = create_engine(f"sqlite:///{self.database}", echo=True)

    def run(self):
        fnames = get_fnames(self.input_path)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        # Открыли сессию для записи
        session = Session()
        for fname in fnames:
            read_path = os.path.join(self.input_path, fname)
            data = pd.read_csv(read_path, compression="gzip")
            for key, value in data.iterrows():
                date = datetime.datetime.strptime(value[1], "%Y-%m-%d %H:%M:%S")
                topic = value[2]
                text = value[3]
                session.add(
                    News(
                        id=str(uuid.uuid4()),
                        date=date,
                        topic=topic,
                        text=text,
                        created_at=datetime.date.today(),
                        updated_at=datetime.date.today(),
                    )
                )

            session.commit()

        # вывод данных из базы. Использовал для тест-проверки
        # for instance in session.query(News).order_by(News.id):
        #    print(instance.id, instance.date, instance.topic, instance.text)

    def requires(self):
        return PreprocessorTask(conf=self.conf)

    def output(self):
        pass


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
        self.classifier_path = self.config["classifier"]["classifier_path"]
        self.ftransformer_path = self.config["classifier"]["ftransformer_path"]

        self.fnames = get_fnames(self.input_path)

    def requires(self):
        return PreprocessorTask(conf=self.conf)

    def run(self):
        logger.info("start %s task", self.__class__.__name__)

        model = joblib.load(self.classifier_path)
        feats_trnsfr = joblib.load(self.ftransformer_path)

        for fname in self.fnames:
            logger.info("process %s", fname)
            readpath = os.path.join(self.input_path, fname)
            writepath = os.path.join(self.output_path, fname)
            data = pd.read_csv(readpath, compression="gzip")
            data.dropna(inplace=True, subset=["lemmatized"])
            feats = feats_trnsfr.transform(data["lemmatized"].values)
            preds = model.predict(feats)
            data["rubric_preds"] = preds
            data[["row_id", "date", "rubric_preds"]].to_csv(writepath, index=False, compression="gzip")

    def output(self):
        outputs = []
        for fname in self.fnames:
            writepath = os.path.join(self.output_path, fname)
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
        # TODO: move model params to the model wrapper script
        self.dict_path = self.config["topic"]["dict_path"]

        self.fnames = get_fnames(self.input_path_c)
        self.class_renamer = json.load(open(os.path.join(os.path.dirname(clf_path), "classnames.json"), "r"))

    def requires(self):
        return RubricClassifierTask(conf=self.conf)

    def make_writepath(self, source_name, cl):
        fname = "{}.csv.gz".format(self.class_renamer[str(cl)])
        dst = os.path.join(self.viz_path, source_name)
        # print(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
        return os.path.join(dst, fname)

    def run(self):
        os.makedirs(os.path.join(self.output_path, "topwords"), exist_ok=True)
        for fname in self.fnames:
            readpath_c = os.path.join(self.input_path_c, fname)
            readpath_l = os.path.join(self.input_path_l, fname)
            data_c = pd.read_csv(readpath_c, compression="gzip")
            data_l = pd.read_csv(readpath_l, compression="gzip")
            data = data_l.merge(data_c[["row_id", "rubric_preds"]], on="row_id", how="inner")
            classes = data["rubric_preds"].unique()
            source_name = fname.split(".")[0]
            for cl in classes:
                tm = topic_model.TopicModelWrapperARTM(self.output_path, source_name + "_" + str(cl))
                mask = data["rubric_preds"] == cl
                # TODO: add option to replace class label by class name
                writepath = self.make_writepath(source_name, cl)
                tm.load_model(
                    os.path.join(self.model_path.format(cl)),
                    os.path.join(self.dict_path.format(cl)),
                )
                tm.prepare_data(data[mask]["lemmatized"].values)
                theta = tm.transform()
                result = theta.merge(
                    data[mask].copy().reset_index()[["date"]],
                    left_index=True,
                    right_index=True,
                )
                tm.save_top_words(os.path.join(self.viz_path, f"tw_{self.class_renamer[str(cl)]}.json"))
                result.to_csv(writepath, compression="gzip", index=False)

    def output(self):
        outputs = []
        for fname in self.fnames:
            readpath_c = os.path.join(self.input_path_c, fname)
            data_c = pd.read_csv(readpath_c, compression="gzip")
            classes = data_c["rubric_preds"].unique()
            for cl in classes:
                source_name = fname.split(".")[0]
                writepath = self.make_writepath(source_name, cl)
                outputs.append(luigi.LocalTarget(writepath))
        return outputs
