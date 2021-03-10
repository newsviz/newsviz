# Copyright © 2021 Andrey Lukyanenko. All rights reserved.
# -*- coding: utf-8 -*-
import configparser
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
import utils
from altair import Chart


@st.cache(allow_output_mutation=True)
def get_data(config_path: str) -> Tuple[Dict, str, str, Dict]:
    """
    Load the data.

    Args:
        config_path: path to the config

    Returns:

    """
    config = configparser.ConfigParser()
    print(config_path)
    config.read(config_path)
    print(list(config.keys()))
    data_path = config["visualizer"]["data_path"]
    loaded_container = utils.load_data(data_path)
    print(list(loaded_container.keys()))
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
