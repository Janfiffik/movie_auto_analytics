import sqlite3
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# ---------------------data load and filtering-------------------------------


def data_by_boolean(data_to_filter, column_name, conditions: list):
    """
    For returning filtered DataFrame by column name and conditions.
    :param data_to_filter: Add DataFrame to filter and get new variable with filtered DataFrame.
    :param column_name:    Column name inside DataFrame.
    :param conditions:     Condition operators for filter. ('equal', 'not_equal', 'higher',
                                                            'lower', 'higher_equal', 'lower_equal')
    :return:               Return filtered DataFrame by boolean indexing
    """
    operator_mapping = {
        "equal": "==",
        "not_equal": "!=",
        "higher": ">",
        "lower": "<",
        "higher_equal": ">=",
        "lower_equal": "<="
    }
    if conditions[1] == str:
        comparison_operator = operator_mapping[conditions[0]]
        comparison_value = conditions[1]
        index = eval(f"data_to_filter['{column_name}'] {comparison_operator} '{comparison_value}'")
        return data_to_filter[index]

    elif conditions[1] == str or float:
        comparison_operator = operator_mapping[conditions[0]]
        comparison_value = conditions[1]
        index = eval(f"data_to_filter['{column_name}'] {comparison_operator} {comparison_value}")
        return data_to_filter[index]


def raw_pandas_df(path):
    """Function that reads file.db and returns pandas dataframe.
       :param path: file path for .db file you want to return as pandas DataFrame.
    """
    connection = sqlite3.connect(path)
    query = "SELECT * FROM movies"
    data_from_db = pd.read_sql_query(query, connection)
    return data_from_db


def group_data(data_to_group, column_names: list):
    """Function accepts pandas DataFrame and group them accordingly by column names,
       :param data_to_group: pandas DataFrame
       :param column_names: list(with column names)
    """
    grouped_data = data_to_group[column_names]
    return grouped_data

# ----------------------------Data Plots-------------------------------


def bar_plot(data, x_col, y_col, mk_color, text_column, plot_title, x_title, y_title, col_ax_title):
    """
    Function for plotting bar chart from DataFrame
    :param data:              Pandas.DataFrame or dictionary to plot
    :param x_col:             Name of the key/column from dictionary or DataFrame.
    :param y_col:             Name of the key/column from dictionary or DataFrame.
    :param mk_color:          Name of the key/column for bar colors.
    :param text_column:       Name of the key/column for text inside bars.
    :param plot_title:        Name of the whole plot.
    :param x_title:           Name of the x-axis.
    :param y_title:           Name of the y-axis.
    :param col_ax_title:      Name inside x-column
    :return:                  Returns plot object.
    """
    fig = go.Figure(go.Bar(x=data[x_col],
                           y=data[y_col],
                           marker_color=data[mk_color],
                           text=data[text_column],
                           textposition='auto',
                           ))
    fig.update_layout(
        autosize=True,
        title=plot_title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        coloraxis_colorbar=dict(title=col_ax_title),
        plot_bgcolor='rgb(205, 205, 255)',
        paper_bgcolor="rgb(215, 215, 255)"
    )
    return fig


def line_plot(data, x_column, y_column, mk_color, line_shape,
              plot_title, x_title, y_title, column_ax_title):
    """
    Function for plotting line chart from DataFrame
    :param data:              Pandas.DataFrame or dictionary to plot
    :param x_column           Name of the column for x-axis.
    :param line_shape:        Set shape of the line for different data in dataframe.
                              Possible values: ("solid", "dot", "dash", "longdash", "dashdot", "longshot")
    :param y_column:          Name of the key/column from dictionary or DataFrame.
    :param mk_color:          Name of the key/column for bar colors.
    :param plot_title:        Name of the whole plot.
    :param x_title:           Name of the x-axis.
    :param y_title:           Name of the y-axis.
    :param column_ax_title:   Name inside x-column
    :return:                  Returns plot object.
    """
    fig = px.line(data,
                  x=x_column,
                  y=y_column,
                  )
    fig.update_layout(
        autosize=True,
        title=plot_title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        coloraxis_colorbar=dict(title=column_ax_title),
        plot_bgcolor='rgb(205, 205, 255)',
        paper_bgcolor="rgb(215, 215, 255)"
    )
    return fig
