import sqlite3
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def raw_pandas_df(path):
    """Function that reads file.db and returns pandas dataframe.
       path: file path for .db file you want to return as pandas DataFrame.
    """
    connection = sqlite3.connect(path)
    query = "SELECT * FROM movie_database"
    data_from_db = pd.read_sql_query(query, connection)
    return data_from_db


def group_data(data_to_group, column_names: list):
    """Function accepts pandas DataFrame and group them accordingly by column names,
       data_to_group: pandas DataFrame
       column_names: list(with column names)
    """
    grouped_data = data_to_group[column_names]
    return grouped_data


def bar_plot(data, x_col, y_col, mk_color, text, title, x_title, y_title, col_ax_title):
    """

    :param data:              Pandas.DataFrame or dictionary to plot
    :param x_col:             Name of the key/column from dictionary or DataFrame.
    :param y_col:             Name of the key/column from dictionary or DataFrame.
    :param mk_color:          Name of the key/column for bar colors.
    :param text:              Name of the key/column for text inside bars.
    :param title:             Name of the whole plot.
    :param x_title:           Name of the x-axis.
    :param y_title:           Name of the y-axis.
    :param col_ax_title:
    :return:
    """
    fig = go.Figure(go.Bar(x=data[x_col],
                           y=data[y_col],
                           marker_color=data[mk_color],
                           text=data[text],
                           textposition='auto',
                           ))
    fig.update_layout(
        autosize=True,
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        coloraxis_colorbar=dict(title=col_ax_title),
        plot_bgcolor='rgb(205, 205, 255)',
        paper_bgcolor="rgb(215, 215, 255)"
    )
    return fig
