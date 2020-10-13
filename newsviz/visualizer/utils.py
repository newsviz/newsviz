import json
import os
from pathlib import Path

import colorlover as cl
import numpy as np
import pandas as pd
import plotly.graph_objs as go

colors = cl.to_rgb(cl.interp(cl.scales["12"]["qual"]["Paired"], 20))
add_colors = cl.to_rgb(cl.scales["7"]["qual"]["Set1"])

# source -> rubrics -> topics
# source is defined by directory name
# rubrics are defined by filenames in dir
# topics are defined by columns' names


def load_data(path):
    """loads data into container
    source -> rubrics -> topics data and topics names
    result is dict like this:
    {'ria': {'sport: (pd.DataFrame(), [topic_1, topic_2]), ...}, ...}
    {source: {rubric: (df with topic values, list of topic_names)
    source is defined by directory name
    rubrics are defined by filenames in dir
    topics are defined by columns' names
    """
    sources = os.listdir(path)
    # check, if only directories included
    sources = [s for s in sources if os.path.isdir(os.path.join(path, s))]
    container = {source: dict() for source in sources}
    for source in sources:
        rubric_files = os.listdir(os.path.join(path, source))
        for fname in rubric_files:
            print(os.path.join(path, source, fname))
            data = pd.read_csv(os.path.join(path, source, fname), compression="gzip")
            data, topics = preprocess_data(data)
            container[source][fname.split(".")[0]] = (data, topics)

    return container


def preprocess_data(df):
    """makes date column from year and month
    scales data by it's std and magic constant 50
    (scaled to offset in ridgeline plot)
    """
    df["date"] = ["{}-{:02d}-01".format(a, b) for a, b in df[["year", "month"]].values]
    df = df.drop(columns=["year", "month"])
    topics = list(df.columns)
    topics.remove("date")
    # scale columns
    maxes = df[topics].max().values
    df[topics] = 50 * df[topics] / np.std(maxes)
    return df, topics


def load_top_words(container):
    top_words = dict()
    # pic first source, assuming all sources have same rubric list
    source = list(container.keys())[0]
    for rubric in container[source].keys():
        top_words[rubric] = json.load(open("./data/tw_{}.json".format(rubric)))
    return top_words


def bump_chart(df, topics):
    pass


# TODO: rewrite this
#     data = list()

#     df1 = df.unstack(level=-1)["mentions"][topics_numbers].rank(axis=1)
#     for topic in topics_numbers:
#         trace = go.Scatter(
#             x=df1.index,
#             y=df1[topic],
#             mode="lines + markers",
#             line=dict(shape="spline", smoothing=1.0, width=5),
#             marker=dict(symbol="circle-open-dot", line=dict(width=7)),
#             hoverinfo="text + x + name",
#             hovertext=df.xs(topic, level=1)["mentions"].values,
#             name=topics_dict[heading][topic],
#         )
#         data.append(trace)

#     height = min(300 + (len(data) * 50), 900)
#     layout = go.Layout(
#         height=height,
#         xaxis=dict(rangeslider=dict(visible=True), type="date"),
#         yaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             showline=False,
#             ticks="",
#             showticklabels=False,
#         ),
#         legend=dict(),
#     )
#     figure = go.Figure(data=data, layout=layout)
#     return figure


def ridge_plot(df, topics, offset=100, add_offset=10):
    """
    df: pandas DataFrame with columns date (type: datetime)
        and columns listed in parameter topics (list of str),
        each topic column of numerical type, float or int
    topics: list of column names to draw
    offset: shift between every single plot (multiplicative)
    add_offset: additive shift
    """
    # data that will be passed to plotly
    data = list()
    for idx, topic in enumerate(topics):
        offset = idx * offset + add_offset
        # filling under line
        tracex = go.Scatter(
            x=df.date.values,
            y=np.full(len(df[topic].values), offset),
            mode=None,
            visible=True,
            legendgroup=str(idx),
            showlegend=False,
            hoverinfo="skip",
            name=f"{topic}_ox",
            line=dict(color=colors[idx]),
            opacity=0.0,
        )
        # line
        trace = go.Scatter(
            x=df.date.values,
            y=df[topic].values + offset,
            fill="tonexty",
            mode=None,
            legendgroup=str(idx),
            hoverinfo="text + name",
            name=topic,
            line=dict(color=colors[idx]),
            opacity=0.0,
        )
        data.append(tracex)
        data.append(trace)

    count_of_plots = len(data)
    # Please someone describe how this computed
    height = min(300 + (count_of_plots // 2 * 50), 900)
    layout = go.Layout(
        height=height,
        xaxis=dict(
            rangeslider=dict(range=[df["date"].min(), df["date"].max()], visible=True),
            type="date",
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        legend=dict(),
    )
    figure = go.Figure(data=data, layout=layout)
    return figure
