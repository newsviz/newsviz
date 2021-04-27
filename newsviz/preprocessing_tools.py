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
from functools import lru_cache
from typing import Optional

import pymorphy2
from loguru import logger

morph = pymorphy2.MorphAnalyzer()


def clean_text(text: str, language: str) -> (Optional[str]):
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
        text = re.sub(r'["`“”:;\.,<>!?\&@\[\]/^_\*\{\}~—–\-«»\(\)]', "", text)  # remove punctuation

        if language == "ru":
            text = re.sub(r"ё", "е", text)
        elif language == "en":
            pass

        text = re.sub(r"\s+", " ", text)  # remove the long blanks

        return text.strip()

    else:
        logger.error("input text only filled string")


@lru_cache()
def get_morph4token(token: str) -> (str):
    """
    get lemma for one tokens with decorator `@lru_cache`
    """

    return morph.parse(token)[0].normal_form


def lemmatize(text: str, language: str, char_for_split: str = " ") -> (Optional[str]):
    """
    lemmatize text with cache
    args:
        input_text (string)
            cleaned text
        language (string)
            "ru" or "en"
        char_for_split (string = " ")
            char-symbol how to split text
    returns:
        lemmatized text
    """

    if (text is not None) and (text != ""):

        # read stopwords
        # TODO: make stopwords path as parameter
        try:
            with open(f"stopwords/sw_{language}.txt", "r") as file:
                stopwords = file.read().splitlines()
        except FileNotFoundError:
            logger.error("can't load stopwords file. maybe parameter `language` not correctly")
            stopwords = []

        list_tokens = text.split(char_for_split)

        if language == "ru":

            words_lem = [get_morph4token(token) for token in list_tokens if token not in stopwords]

        elif language == "en":

            pass

        if len(words_lem) > 3:
            return " ".join(words_lem)
        else:
            return ""

    else:
        logger.error("input text only filled string")
