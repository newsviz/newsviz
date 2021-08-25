import argparse
import configparser
import os

import pandas as pd
from preprocessing_tools import Preprocessing
from search import engine
from topic_model import TopicModelWrapperARTM


class SearchWrapper:
    def __init__(self):
        conf_path = "../config/search_config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(conf_path)
        self.input_path = self.config["common"]["raw_path"]
        self.model_path = self.config["topic"]["model_path"]
        self.output_path = self.config["topic"]["output_path"]
        self.dict_path = self.config["topic"]["dict_path"]
        self.language = self.config["preprocessor"]["language"]
        self.vec_path = self.config["topic"]["vec_path"]
        self.dataset_name = self.config["topic"]["dataset_name"]

        self._get_vectors()
        self._load_model()

    def _load_model(self, cl=0):
        self.model = TopicModelWrapperARTM(self.output_path, self.dataset_name, len(self.embs[0]))
        self.model.load_model(
            os.path.join(self.model_path.format(cl)),
            os.path.join(self.dict_path.format(cl)),
        )

    def _get_input_vector(self, input_text):
        preprocess = Preprocessing(language=self.language)
        cleaned_text = preprocess.clean_text(input_text)
        lemmatized_text = preprocess.lemmatize(cleaned_text)
        self.model.prepare_data([lemmatized_text])
        return self.model.transform().values[0]

    def _get_vectors(self):
        self.embs = pd.read_csv(self.vec_path, compression="gzip")
        self.embs = self.embs.drop("date", axis=1).values

    def get_nearest_news(self, query, topn):
        query_vec = self._get_input_vector(query)
        meta = pd.read_csv(self.input_path, compression="gzip")["text"].values
        ranker = engine.Ranker(self.embs, meta)
        nearest_news_ids = ranker.get_nearest(query_vec, topn)
        return ranker.get_attributes(nearest_news_ids)


def get_nearest_news(query, topn):
    search = SearchWrapper()
    nearest_news = search.get_nearest_news(query, topn)
    print(nearest_news)
    return nearest_news


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", dest="query", type=str, default="", help="The query for the topic model inference")
    parser.add_argument("--top_n", dest="top_n", type=int, default=10, help="Number of the nearest news to return")

    args = parser.parse_args()
    get_nearest_news(
        args.query,
        args.top_n,
    )
