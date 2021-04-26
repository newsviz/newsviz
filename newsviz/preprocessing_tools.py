# Copyright © 2021 @vtrokhymenko. All rights reserved.
# Copyright © 2020 Viktor Trokhymenko. All rights reserved.
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
from functools import lru_cache

from typing import Optional
from loguru import logger

import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def clean_text(text: str, language) -> (Optional[str]):
    """
    clean text, leaving only tokens for clustering
    args:
        text (string)
            input text
        language (string)
            "ru" or "en"
    returns:
        cleaned string text without lower case
    """

    if (text is not None) and (text != ""):

        text = html.unescape(text)

        text = re.sub(r"http\S+", "", text)  # remove urls
        text = re.sub(r"\S+@\S+", "", text)  # remove emails
        text = re.sub(
            r"\!|\"|\:|\;|\.|\,|[<>]|\?|\@|\[|\]|\^|\_|\`|\*|/|[{}]|\~|[—–-]|[«»]|[()]|[>]|[“”]", " ", text
        )  # remove punctuation

        if language == "ru":
            text = re.sub(r"ё", "е", text)

        if language == "en":
            pass

        text = re.sub(r"\s+", " ", text)  # remove the long blanks

        text = text.strip()

        if len(text) < 3:
            return ""
        else:
            return text
    else:
        logger.error("input text only filled string")


@lru_cache()
def get_morph4token(token: str) -> (str):
    """
    get lemma for one tokens with decorator `@lru_cache`
    """

    return morph.parse(token)[0].normal_form


def lemmatize(text: str, language: str = "ru", char4split: str = " ") -> (Optional[str]):
    """
    lemmatize text with cache
    args:
        input_text (string)
            cleaned text
        language (string)
            "ru" or "en"
        char4split (string = " ")
            char-symbol how to split text
    returns:
        lemmatized text
    """

    if (text is not None) and (text != ""):

        # get tokens from input text
        # in this case it's normal approach because we hard cleaned text
        list_tokens = text.split(char4split)
        if language != "ru":

            # TODO: make this a parameter
            stopwords_path = "stopwords_ru.txt"
            try:
                with open(stopwords_path, "r") as file:
                    stopwords = file.read().splitlines()
            except FileNotFoundError:
                logger.error("can't load stopwords file")
                stopwords = []

            words_lem = [get_morph4token(token) for token in list_tokens if token not in stopwords]

        if language == "en":

            # TODO: make this a parameter
            stopwords_path = "stopwords_en.txt"
            try:
                with open(stopwords_path, "r") as file:
                    stopwords = file.read().splitlines()
            except FileNotFoundError:
                logger.error("can't load stopwords file")
                stopwords = []

        if len(words_lem) < 3:
            return ""
        else:
            return " ".join(words_lem)

    else:
        logger.error("input text only filled string")
