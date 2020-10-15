import configparser
import logging
import os
import sys
import json

import joblib
import luigi
import pandas as pd
import topic_model
from preprocessing_tools import clean_text
from preprocessing_tools import lemmatize


def get_fnames(path):
    fnames = []
    for item in os.listdir(path):
        if os.path.isdir(item) or not item.endswith(".csv.gz"):
            continue
        fnames.append(item)
    return fnames


class PreprocessorTask(luigi.Task):
    """ expects directory with csv files in it
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
        for fname in self.fnames:
            readpath = os.path.join(self.input_path, fname)
            writepath = os.path.join(self.output_path, fname)
            data = pd.read_csv(readpath, compression="gzip")
            data["cleaned_text"] = data["text"].apply(clean_text)
            data["lemmatized"] = data["cleaned_text"].apply(lemmatize)
            data["row_id"] = np.arange(data.shape[0])
            data[["row_id", "date", "topics", "lemmatized"]].to_csv(
                writepath, index=False, compression="gzip"
            )

    def output(self):
        outputs = []
        for fname in self.fnames:
            writepath = os.path.join(self.output_path, fname)
            outputs.append(luigi.LocalTarget(writepath))
        return outputs


class RubricClassifierTask(luigi.Task):
    """ depends on previous step
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
        model = joblib.load(self.classifier_path)
        feats_trnsfr = joblib.load(self.ftransformer_path)

        for fname in self.fnames:
            readpath = os.path.join(self.input_path, fname)
            writepath = os.path.join(self.output_path, fname)
            data = pd.read_csv(readpath, compression="gzip")
            data.dropna(inplace=True, subset=["lemmatized"])
            feats = feats_trnsfr.transform(data["lemmatized"].values)
            preds = model.predict(feats)
            data["rubric_preds"] = preds
            data[["row_id", "date", "rubric_preds"]].to_csv(
                writepath, index=False, compression="gzip"
            )

    def output(self):
        outputs = []
        for fname in self.fnames:
            writepath = os.path.join(self.output_path, fname)
            outputs.append(luigi.LocalTarget(writepath))
        return outputs


class TopicPredictorTask(luigi.Task):
    """ depends on previous step
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
        self.viz_path = self.config['visualizer']['data_path']
        clf_path = self.config['classifier']['classifier_path']
        # TODO: add class to classname mapping
        # TODO: move model params to the model wrapper script
        self.dict_path = self.config["topic"]["dict_path"]

        self.fnames = get_fnames(self.input_path_c)
        self.class_renamer = json.load(open(os.path.join(os.path.dirname(clf_path),
             'classnames.json'), 'r'))


    def requires(self):
        return RubricClassifierTask(conf=self.conf)

    def make_writepath(self, source_name, cl):
        fname = '{}.csv.gz'.format(self.class_renamer[str(cl)])
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
            data = data_l.merge(data_c[['row_id', 'rubric_preds']], on='row_id', how='inner')
            classes = data["rubric_preds"].unique()
            source_name = fname.split(".")[0]
            for cl in classes:
                tm = topic_model.TopicModelWrapperARTM(self.output_path, source_name + "_" + str(cl))
                mask = data["rubric_preds"] == cl
                # TODO: add option to replace class label by class name
                writepath = self.make_writepath(source_name, cl)
                tm.load_model(
                    os.path.join(self.model_path.format(cl)),
                    os.path.join(self.dict_path.format(cl))
                )
                tm.prepare_data(data[mask]["lemmatized"].values)
                theta = tm.transform()
                result = theta.merge(
                    data[mask].copy().reset_index()[["date"]],
                    left_index=True,
                    right_index=True,
                )
                tm.save_top_words(
                    os.path.join(self.viz_path, f"tw_{self.class_renamer[str(cl)]}.json")
                )
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
