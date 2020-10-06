import os
from pathlib import Path
import json

import artm
import numpy as np
import pandas as pd


class TopicModelWrapperARTM:
    def __init__(self, dir_path, name_dataset, n_topics=50):
        """ dir_path: path to directory where all outputs
                and temporary files should be stored
            name_dataset: used to generate paths and file names
            n_topics: number of topics in topic model
        """
        self.dir_path = dir_path
        self.name_dataset = name_dataset
        self.vwpath = f"{dir_path}/vwpath/{name_dataset}_input_bigartm.vw"
        self.model = None
        self.n_topics = n_topics
        self.dictionary_path = None

    # data, n_topics = 50
    def prepare_data(self, data):
        """
        data -- array of tokenized text
        """
        self.vwpath_dir = f"{self.dir_path}/vwpath/"
        if not os.path.exists(self.vwpath_dir):
            print("creating vw path...\n")
            os.makedirs(self.vwpath_dir)

        with open(self.vwpath, "w") as fp:
            for i, text in enumerate(data):
                fp.write("{} |default {}\n".format(i, text))

        self.batches_path = f"{self.dir_path}/batches/{self.name_dataset}"

        if not os.path.exists(self.batches_path):
            print("creating batches path...\n")
            os.makedirs(self.batches_path)

        self.batch_vectorizer = artm.BatchVectorizer(
            data_path=self.vwpath,
            data_format="vowpal_wabbit",
            target_folder=self.batches_path,
            gather_dictionary=False,
        )

        if not os.path.exists(f"{self.dir_path}/dicts/"):
            print("creating dicts path...\n")
            print(f"{self.dir_path}/dicts/")
            os.makedirs(f"{self.dir_path}/dicts/")

    def init_model(self, dictionary_path=None):
        """ dictionary_path: optional, used with pretrained model
        """
        self.dictionary = artm.Dictionary()
        if dictionary_path is None:
            self.dictionary.gather(data_path=self.batches_path)
            self.dictionary.filter(min_tf=10, max_df_rate=0.1)
            self.dictionary.save_text(
                f"{self.dir_path}/dicts/dict_{self.name_dataset}.txt")
        else:
            self.dictionary.load_text(dictionary_path)

        self.model = artm.ARTM(num_topics=self.n_topics,
                               dictionary=self.dictionary,
                               show_progress_bars=True)

        # scores
        self.model.scores.add(
            artm.PerplexityScore(name="PerplexityScore",
                                 dictionary=self.dictionary))
        self.model.scores.add(
            artm.SparsityThetaScore(name="SparsityThetaScore"))
        self.model.scores.add(artm.SparsityPhiScore(name="SparsityPhiScore"))

        # regularizers
        self.model.regularizers.add(
            artm.SmoothSparsePhiRegularizer(name="SparsePhi", tau=-0.1))
        self.model.regularizers.add(
            artm.SmoothSparseThetaRegularizer(name="SparseTheta", tau=-0.5))
        self.model.regularizers.add(
            artm.DecorrelatorPhiRegularizer(name="DecorrelatorPhi", tau=1.5e5))

    def fit(self):
        if self.model is None:
            self.init_model()
        self.model.fit_offline(batch_vectorizer=self.batch_vectorizer,
                               num_collection_passes=50)

        sparsityTheta = self.model.score_tracker[
            "SparsityThetaScore"].last_value
        sparsityPhi = self.model.score_tracker["SparsityPhiScore"].last_value
        perpl = self.model.score_tracker["PerplexityScore"].last_value

        print(f"\tSparsityThetaScore: {sparsityTheta}")
        print(f"\tSparsityPhiScore: {sparsityPhi}")
        print(f"\tPerplexityScore: {perpl}")

    def get_phi(self):
        assert not (self.model is None), "init and fit (or load) model first"
        phi = self.model.get_phi()
        phi["word"] = phi.index
        return phi

    def print_top_words(self):
        phi = self.get_phi()
        for topic in phi.columns:
            print(topic)
            top_words = (phi.sort_values(
                by=topic,
                ascending=False)["word"].apply(lambda x: x[1]).values[:20])
            print(top_words)
            print("==" * 5)

    def save_model(self, path):
        """ path: path to save model"""
        model_path = Path(path)
        dict_path = model_path.parent / f"dictionary_{model_path.stem}.txt"
        self.dictionary.save_text(str(dict_path))
        self.model.save(path)

    def load_model(self, path, dictionary_path):
        """ path: path to model binary saved with 'save_model'
            dictionary_path: path to dictionary for this model
        """
        # TODO: make dictionary path from model path
        if self.model is None:
            self.init_model(dictionary_path)
        self.dictionary_path = dictionary_path
        self.model.load(path)

    def transform(self):
        if self.model is None:
            raise Exception("init and fit (or load) model first")
        theta = self.model.transform(batch_vectorizer=self.batch_vectorizer)
        theta = theta.T
        return theta

    def save_top_words(self, path, top=20):
        """ path: where to save top words
            top: number top words to save
        """
        phi = self.get_phi()
        top_words_dict = dict()
        for topic in phi.columns.drop('word'):
            top_words = (phi.sort_values(
                by=topic,
                ascending=False)["word"].values[:top])
            top_words_dict[topic] = list(top_words)

        json.dump(top_words_dict, open(path, "w"))
