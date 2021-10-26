# Copyright © 2021 @vtrokhymenko. All rights reserved.
# Copyright © 2021 Andrey Lukyanenko. All rights reserved.
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
import argparse

import streamlit as st
from st_app_functions import get_data
from st_app_functions import make_plot
from st_app_functions import update_data

# According to https://github.com/streamlit/streamlit/issues/337
# run it like this:
# streamlit run st_app.py -- --config_path /path/to/config

parser = argparse.ArgumentParser(description="Streamlip app")
parser.add_argument("--config_path", help="path to config", type=str, default="../config/config.ini")

args = parser.parse_args()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
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

    st.plotly_chart(figure, use_container_width=True)
    st.header("Топ слов по темам")
    st.subheader(rubric)
    st.dataframe(top_words_df)
