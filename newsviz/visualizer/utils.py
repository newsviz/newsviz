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
            # print(data.head())
            data, topics = preprocess_data(data)
            container[source][fname.split(".")[0]] = (data, topics)

    return container


def preprocess_data(df):
    """makes date column from year and month
    scales data by it's std and magic constant 50
    (scaled to offset in ridgeline plot)
    """
    topics = list(df.columns)
    topics.remove("date")
    # scale columns
    maxes = df[topics].max().values
    df[topics] = df[topics] / np.std(maxes)
    return df, topics


def load_top_words(container, path):
    top_words = dict()
    # pick first source, assuming all sources have same rubric list
    source = list(container.keys())[0]
    for rubric in container[source].keys():
        path_json = os.path.join(path, f"tw_{rubric}.json")
        with open(path_json, "r") as f:
            top_words[rubric] = json.load(f)
    return top_words


def aggregate_by_date(df, level="month"):
    """
    df: pandas DataFrame with columns date (type: datetime)
        and columns listed in parameter topics (list of str),
        each topic column of numerical type, float or int
    level: str of level of aggregation (hour, day, week, month or year),
    """
    #  remove after fix preprocess_data()
    df["date"] = pd.to_datetime(df["date"])
    level_to_freq = {
        "hour": "1H",
        "day": "1D",
        "week": "1W",
        "month": "1MS",  # month start
        "year": "1YS",  # year start
    }
    freq = level_to_freq.get(level)
    if freq is None:
        raise ValueError(f"'level' must be one of {list(level_to_freq.keys())}")
    grouper = pd.Grouper(key="date", freq=level_to_freq[level])
    dfgb = df.groupby(grouper).sum().reset_index()
    return dfgb


def compute_figure_height(count_of_plots):
    # values are selected empirically
    MIN_HEIGHT = 300
    MAX_HEIGHT = 900
    PLOT_HEIGHT = 50
    return min(MIN_HEIGHT + (count_of_plots * PLOT_HEIGHT), MAX_HEIGHT)


def bump_chart(df, topics):
    """
    df: pandas DataFrame with columns date (type: datetime)
        and columns listed in parameter topics (list of str),
        each topic column of numerical type, float or int
    topics: list of column names to draw
    """
    data = list()
    df_plot = df.loc[:, topics].rank(axis=1, method="max").astype(int)
    df_plot["date"] = df["date"]
    for idx, topic in enumerate(topics):
        trace = go.Scatter(
            x=df_plot["date"],
            y=df_plot[topic].values,
            mode="lines",
            line=dict(shape="spline", smoothing=1.0, width=3),
            marker=dict(symbol="circle-open-dot", line=dict(width=7)),
            hoverinfo="name",
            name=topic,
        )
        data.append(trace)
    count_of_plots = len(data)
    height = compute_figure_height(count_of_plots)
    layout = go.Layout(
        height=height,
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        legend=dict(),
        hovermode="x",
    )
    figure = go.Figure(data=data, layout=layout)
    return figure


def compute_offset(df, topics):
    return np.max(df[topics].max()) * 0.85


def ridge_plot(df, topics, add_offset=100):
    """
    df: pandas DataFrame with columns date (type: datetime)
        and columns listed in parameter topics (list of str),
        each topic column of numerical type, float or int
    topics: list of column names to draw
    offset: shift between every single plot (multiplicative)
    add_offset: additive shift
    """
    offset = compute_offset(df, topics)
    # data that will be passed to plotly
    data = list()
    for idx, topic in enumerate(topics):
        y_offset = idx * offset + add_offset
        # filling under line
        tracex = go.Scatter(
            x=df["date"],
            y=np.full(len(df[topic].values), y_offset),
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
            x=df["date"],
            y=df[topic].values + y_offset,
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

    # div by 2 -- each plot is formed by two traces
    count_of_plots = len(data) // 2
    height = compute_figure_height(count_of_plots)
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
        hovermode="x",
    )
    figure = go.Figure(data=data, layout=layout)
    return figure
