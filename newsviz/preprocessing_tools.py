# Copyright © 2020, 2021 @vtrokhymenko. All rights reserved.
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

import html
import re
from dataclasses import InitVar, dataclass, field
from functools import lru_cache
from typing import List, Optional

import spacy
from loguru import logger


@dataclass
class Preprocessing:
    """
    args:
        language (string = "ru"):
            "ru" or "en"
        stopwords (List[str] = [])
        replace_path_stopwords_4_tests (InitVar[bool] = False)
        nlp: (spacy.lang = None)
    """

    language: str = "ru"
    stopwords: List[str] = field(default_factory=list)
    replace_path_stopwords_4_tests: InitVar[bool] = False
    nlp: spacy.lang = None

    def __post_init__(self, replace_path_stopwords_4_tests):
        """
        in folder news/stopwords be 2 files: `sw_ru.txt` & `sw_en.txt`
        for lemmatizer for your language u should download spacy trained pipelines
            $ python -m spacy download ru_core_news_md
            or
            $ python -m spacy download en_core_web_md
        """
        # read stopwords
        # TODO: make stopwords path as parameter
        try:
            if replace_path_stopwords_4_tests:
                path_stopwords = f"newsviz/stopwords/sw_{self.language}.txt"
            else:
                path_stopwords = f"./stopwords/sw_{self.language}.txt"

            with open(path_stopwords, "r") as file:
                self.stopwords = file.read().splitlines()
        except FileNotFoundError:
            logger.error("can't load stopwords file. maybe parameter `language` not correctly\n")
            self.stopwords = []

        print(f"{len(self.stopwords) = }")

        # load lemmatizer
        if self.language == "ru":
            spacy_pipeline = "ru_core_news_md"
        elif self.language == "en":
            spacy_pipeline = "en_core_web_md"

        self.nlp = spacy.load(spacy_pipeline)

    def clean_text(self, text: str) -> (Optional[str]):
        """
        clean text, leaving only tokens for clustering
        args:
            text (string)
                input text
        returns:
            cleaned string text without lower case
        """

        if (text is not None) and (text != ""):

            text = html.unescape(text)

            text = re.sub(r"http\S+", "", text)  # remove urls
            text = re.sub(r"\S+@\S+", "", text)  # remove emails
            text = re.sub(r'["`“”:;\.,<>!?\&@\[\]/^_\*\{\}~—–\-«»\(\)]', "", text)  # remove punctuation

            if self.language == "ru":
                text = re.sub(r"ё", "е", text)
            elif self.language == "en":
                pass

            text = re.sub(r"\s+", " ", text)  # remove the long blanks

            return text.strip()

        else:
            logger.error("input text only filled string\n")

    # @property
    # @lru_cache()
    # def get_spacy_lemma_from_token(token: spacy.tokens.token.Token) -> (str):
    #     """
    #     get lemma for one tokens with decorator `@lru_cache`
    #     """

    #     return token.lemma_

    def lemmatize(self, text: str) -> (Optional[str]):
        """
        lemmatize text with cache
        args:
            input_text (string)
                cleaned text
        returns:
            lemmatized string text
        """
        if (text is not None) and (text != ""):

            doc = self.nlp(text)

            words_lem = [token.lemma_ for token in doc if str(token) not in self.stopwords]
            # words_lem = [get_spacy_lemma_from_token(token) for token in doc if str(token) not in self.stopwords]

            return " ".join(words_lem).lower()

        else:
            logger.error("input text only filled string")
