# Copyright © 2021 Andrey Lukyanenko. All rights reserved.
# -*- coding: utf-8 -*-
import argparse

import streamlit as st
from st_app_functions import get_data, make_plot, update_data

if __name__ == "__main__":
    """
    Example of usage:
    >>> python st_app.py
    """

    parser = argparse.ArgumentParser(description="Streamlip app")
    parser.add_argument("--config_path", help="path to config", type=str, default="config/config.ini")

    args = parser.parse_args()

    st.title("NewsViz Project")

    container, source0, rubric0, top_words = get_data(args.config_path)

    # selectors
    option = st.sidebar.selectbox("Источник", ([s for s in container.keys()]))
    type_chart = st.sidebar.selectbox("Тип Графика", ("Ridge plot", "Bump chart"))
    rubric = st.sidebar.selectbox("Рубрика", ([s for s in container[source0].keys()]))
    topic = st.sidebar.multiselect(
        "Темы", ([s for s in container[source0][rubric0][1]]), default=["topic_0", "topic_1"]
    )
    agg_level = st.sidebar.selectbox(
        "Уровень аггрегации",
        (["month", "hour", "day", "week", "year"]),
        format_func=lambda x: x.capitalize(),
    )

    df, top_words_df = update_data(container, option, rubric, agg_level, top_words, topic)

    # show the results
    figure = make_plot(type_chart, df, topic)

    st.plotly_chart(figure)
    st.header("Топ слов по темам")
    st.subheader(rubric)
    st.dataframe(top_words_df)
