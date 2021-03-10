# Copyright © 2021 Andrey Lukyanenko. All rights reserved.
# -*- coding: utf-8 -*-


import configparser
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
import utils
from altair import Chart


@st.cache(allow_output_mutation=True)
def get_data() -> Tuple[Dict, str, str, Dict]:
    """
    Load the data

    """
    PATH_CONFIG = "../config/config.ini"
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    data_path = config["visualizer"]["data_path"]
    loaded_container = utils.load_data(data_path)

    source0 = list(loaded_container.keys())[0]
    rubric0 = list(loaded_container[source0].keys())[0]

    top_words = utils.load_top_words(loaded_container, data_path)

    return loaded_container, source0, rubric0, top_words


@st.cache
def update_data(
    container: Dict, option: str, rubric: str, agg_level: str, top_words: Dict, topic: List
) -> Tuple[pd.DataFrame, Dict]:
    """
    Updates the data which will be shown

    Args:
        container: container from utils
        option: source of the data
        rubric: rubric
        agg_level: aggregation period
        top_words: dictionary with top words
        topic: selected topics

    Returns:

    """
    df, topics = container[option][rubric]
    df = utils.aggregate_by_date(df, level=agg_level)
    top_words_df = pd.DataFrame({t: top_words[rubric][t] for t in sorted(topic)})
    return df, top_words_df


def make_plot(type_chart_: str, df_: pd.DataFrame, topic_: List) -> Chart:
    """
    Makes the plot of the defined type
    Args:
        type_chart_: type of the chart
        df_: dataframe with the data
        topic_: selected topics

    Returns:

    """
    if type_chart_ == "Ridge plot":
        return utils.ridge_plot(df_, topic_)
    elif type_chart_ == "Bump chart":
        return utils.bump_chart(df_, topic_)


st.title("NewsViz Project")

container, source0, rubric0, top_words = get_data()

option = st.sidebar.selectbox("Источник", ([s for s in container.keys()]))
type_chart = st.sidebar.selectbox("Тип Графика", ("Ridge plot", "Bump chart"))
rubric = st.sidebar.selectbox("Рубрика", ([s for s in container[source0].keys()]))
topic = st.sidebar.multiselect("Темы", ([s for s in container[source0][rubric0][1]]), default=["topic_0", "topic_1"])
agg_level = st.sidebar.selectbox(
    "Уровень арргерации",
    (["month", "hour", "day", "week", "year"]),
    format_func=lambda x: x.capitalize(),
)

df, top_words_df = update_data(container, option, rubric, agg_level, top_words, topic)

figure = make_plot(type_chart, df, topic)

st.plotly_chart(figure)
st.header("Топ слов по темам")
st.subheader(rubric)
st.dataframe(top_words_df)
