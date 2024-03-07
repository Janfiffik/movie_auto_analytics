import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def raw_pandas_df(path):
    """Function that reads file.db and returns pandas dataframe.
       path: file path for .db file you want to return as pandas DataFrame.
    """
    connection = sqlite3.connect('instance/moviesDB.db')
    query = "SELECT * FROM movie_database"
    data_from_db = pd.read_sql_query(query, connection)
    return data_from_db

file_path = "C:/Users/Janokop/PycharmProjects/auto_it_analysis/automatic_analysis/application/instance/moviesDB.db"
raw_data = raw_pandas_df(file_path)
print(raw_data.head(3))

