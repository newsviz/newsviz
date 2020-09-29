import html
import re
import sys
from functools import lru_cache
from pathlib import Path

import pymorphy2

PATH = Path("../..")
sys.path.append(str(PATH))

morph = pymorphy2.MorphAnalyzer()

# read stopwords for RU
try:
    with open(PATH / "data/features/stopwords_ru.txt", "r") as file:
        stopwords = file.read().splitlines()
except FileNotFoundError:
    stopwords = []

# create cache
cache = {}


def clean_text(text: str = None) -> str:
    """
    clean text, leaving only tokens for clustering

    Parameters
    ----------
        text : string
            input text

    Returns
    -------
        text : string
            cleaned string text
    """

    if not isinstance(text, str):
        text = str(text)

    text = html.unescape(text)

    text = text.lower()
    text = re.sub(r"[^а-яА-Я\-]+", " ", text)  # leave the Cyrillic alphabet
    # remove the single characters
    text = re.sub(r"(?<!\S).(?!\S)\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()  # remove the long blanks

    if len(text) < 3:
        return "9999"
    else:
        return text


@lru_cache()
def get_morph4token(token: str = None) -> str:
    """
    get lemma for one tokens with lru_cache

    Parameters
    ----------
    token : string
        input word (e.x. from list tokens)
    Returns
    -------
    word_lem : string
        lemmatized text
    """

    return morph.parse(token)[0].normal_form


def lemmatize(text: str = None) -> str:
    """
    lemmatization text with cache

    Parameters
    ----------
    input_text : string
        cleaned text
    Returns
    -------
    words_lem : string
        lemmatized text
    """

    # get tokens from input text
    # in this case it's normal approach because we hard cleaned text
    if not isinstance(text, str):
        text = str(text)

    # get tokens from input text
    # in this case it's normal approach because we hard cleaned text
    list_tokens = text.split(" ")

    words_lem = [
        get_morph4token(token) for token in list_tokens
        if token not in stopwords
    ]

    if len(words_lem) < 3:
        return "9999"
    else:
        return " ".join(words_lem)
