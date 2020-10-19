# -*- coding: utf-8 -*-
# from pathlib import PurePosixPath, Path
import collections
import configparser
import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from plotly import tools
import utils

# TODO: Add top words

PATH_CONFIG = "../config/config.ini"
config = configparser.ConfigParser()
config.read(PATH_CONFIG)
data_path = config["visualizer"]["data_path"]

container = utils.load_data(data_path)
# source -> rubrics -> topics
# source is defined by directory name
# rubrics are defined by filenames in dir
# topics are defined by columns' names
source0 = list(container.keys())[0]  # FE: 'ria'
rubric0 = list(container[source0].keys())[0]  # FE 'sport'
# container = {'ria': {'sport: (pd.DataFrame(), [topic_1, topic_2]), ...}, ...}
# template: {source: {rubric: (df with topic values, list of topic_names)

top_words = utils.load_top_words(container, data_path)

# here is page template ==========================
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Panel with menu on the left of the page
left_panel = html.Div(
    style={"width": "200px", "float": "left"},
    children=[
        # Source choice
        html.Div(
            [
                dcc.Markdown(
                    d(
                        """
                    **Источник**
                """
                    )
                ),
                dcc.Dropdown(
                    id="source",
                    options=[{"label": s, "value": s} for s in container.keys()],
                    value=list(container.keys())[0],
                ),
            ]
        ),
        # Chart type choice
        html.Div(
            [
                dcc.Markdown(
                    d(
                        """
                    **Тип графика**
                """
                    )
                ),
                dcc.Dropdown(
                    id="type_chart",
                    options=[
                        {"label": "Ridge plot", "value": "ridge"},
                        {"label": "Bump chart", "value": "bump"},
                    ],
                    value="ridge",
                ),
            ]
        ),
        # Rubric choice
        html.Div(
            [
                dcc.Markdown(
                    d(
                        """
                    **Рубрики**
                """
                    )
                ),
                dcc.Dropdown(
                    id="rubric",
                    value=list(container[source0].keys())[0],
                    options=[
                        {"label": s, "value": s} for s in container[source0].keys()
                    ],
                ),
            ]
        ),
        # Topic list choice
        html.Div(
            [
                dcc.Markdown(
                    d(
                        """
                    **Темы**
                """
                    )
                ),
                dcc.Dropdown(
                    id="topics",
                    multi=True,
                    value=["topic_0", "topic_1"],
                    options=[
                        {"label": s, "value": s} for s in container[source0][rubric0][1]
                    ],
                ),
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    d(
                        """
                    **Уровень агрегации**
                """
                    )
                ),
                dcc.Dropdown(
                    id="agg_level",
                    value="month",
                    options=[
                        {"label": "Hour", "value": "hour"},
                        {"label": "Day", "value": "day"},
                        {"label": "Week", "value": "week"},
                        {"label": "Month", "value": "month"},
                        {"label": "Year", "value": "year"},
                    ],
                ),
            ]
        ),
    ],
    className="three columns",
)

# Block with main plot
fig_div = html.Div(
    style={"margin-left": "200px"},
    children=[dcc.Graph(id="graph", figure=go.Figure())],
    className="nine columns",
)

# Here is layout of the whole page
app.layout = html.Div(
    children=[
        # Page heading
        html.H1(children="NewsViz Project"),
        # left panel and main plot
        html.Div(children=[left_panel, fig_div]),
        # Table with top words for chosen topics
        html.Div(
            [html.H2(children="Топ слов по темам"), html.Div(id="top_words",)],
            className="twelve columns",
        ),
    ],
    className="twelve columns",
)
# end of page template =======================


# All callbacks ===========
@app.callback(Output("rubric", "options"), [Input("source", "value")])
def update_rubric(source):
    """For given source outputs
        list of available rubrics
        """
    options = [
        {"label": rubric, "value": rubric} for rubric in container[source].keys()
    ]
    return options


@app.callback(
    Output("topics", "options"), [Input("source", "value"), Input("rubric", "value")]
)
def update_topics(source, rubric):
    """For given source and rubric
    outputs list of available topics
    """
    topics = container[source][rubric][1]
    options = [{"label": topic, "value": topic} for topic in topics]
    return options


@app.callback(
    Output("top_words", "children"),
    [Input("source", "value"), Input("rubric", "value"), Input("topics", "value")],
)
def update_top_words(source, rubric, topics):
    """returns table with top words
        for every selected topic
    """
    result = []
    for topic in topics:
        div = html.Div(
            [
                html.H5(children=f"{rubric} {topic}"),
                html.Div(children=", ".join(top_words[rubric][topic])),
            ],
            className="one columns",
        )
        result.append(div)
    return result


@app.callback(
    Output("graph", "figure"),
    [
        Input("source", "value"),
        Input("type_chart", "value"),
        Input("rubric", "value"),
        Input("topics", "value"),
        Input("agg_level", "value"),
    ],
)
def update_graph(source, type_chart, rubric, selected_topics, agg_level):
    """creates a figure for given params"""
    df, topics = container[source][rubric]
    df = utils.aggregate_by_date(df, level=agg_level)
    if type_chart == "ridge":
        figure = utils.ridge_plot(df, selected_topics)
    elif type_chart == "bump":
        # TODO: implement bump_chart
        figure = utils.bump_chart(df, selected_topics)
    # TODO: implement heatmap

    figure["layout"]["xaxis"].update()

    return figure


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)
