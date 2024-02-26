import csv
import random
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time as tm
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def imdb_top_movies():
    """For getting movie list from imdb database by webscraping"""
    url_movies = 'https://www.imdb.com/chart/top/'
    headers = {'User-Agent': 'Chrome/58.0.3029.110', 'Accept-Language': 'en-US,en;q=0.9'}

    response = requests.get(url_movies, headers=headers)
    movies_names = []
    if response.status_code == 200:
        raw_data = BeautifulSoup(response.content, 'html.parser')
        movie_titles = raw_data.find_all(class_='ipc-title-link-wrapper')
        movies_list = [movie.text for movie in movie_titles]
        for movie in movies_list[0:250]:
            movie = (movie.split(' ', 1))
            movies_names.append(movie[1])
    else:
        print("Error: ", response.status_code)
    return movies_names


def movie_json_data(movies_names, api_key="YOUR KEY"):
    """For getting raw JSON data from IMDb database. You need pass as argument list with movie names.
       its creates JSON file.

       !!!!!_You can get your API key by signing in to IMDb database_!!!!!
    """
    movies_data = []
    for movie in movies_names:
        url = 'https://www.omdbapi.com'
        params = {"plot": "full", "apikey": api_key, "type": "movie", "t": movie}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            raw_data = response.json()
            movies_data.append(raw_data)
        else:
            print("Error: ", response.status_code)

    with open("data/movies_raw_data.json", "w") as json_file:
        json.dump(movies_data, json_file, indent=4, separators=(',', ': '))


def movie_prices(movies):
    """It returns 2D list of lists with: budgets_list, gross_us,
       gross_world, opening_us_canada
       Argument accept: list with imdb ID of movies
    """
    budgets_list = []
    gross_us = []
    gross_world = []
    opening_us_canada = []

    for movie in movies:
        url_movie_price = f"https://www.imdb.com/title/{movie}/?ref_=chttp_t_1"
        headers = {'User-Agent': 'Chrome/58.0.3029.110', 'Accept-Language': 'en-US,en;q=0.9'}
        response = requests.get(url_movie_price, headers=headers)
        response_data = BeautifulSoup(response.content, 'html.parser')
        movie_budget_str = response_data.find_all(class_="ipc-metadata-list-item__list-content-item")
        movie_price = [movie.text for movie in movie_budget_str]

        movie_price = [budget.replace(',', "") for budget in movie_price if '$' in budget]
        movie_price = [budget.replace('(estimated)', '') for budget in movie_price]
        movie_price = [budget.replace('$', '') for budget in movie_price]

        try:
            budgets_list.append(movie_price[0])
        except IndexError:
            budgets_list.append("0")
        try:
            gross_us.append(movie_price[1])
        except IndexError:
            gross_us.append("0")
        try:
            opening_us_canada.append(movie_price[2])
        except IndexError:
            opening_us_canada.append("0")
        try:
            gross_world.append(movie_price[3])
        except IndexError:
            gross_world.append("0")
        tm.sleep(random.choice(range(0, 1)))
    return [budgets_list, gross_us, gross_world, opening_us_canada]


def data_type_test(input_data, head=5):
    """Prints first 3 rows from DataFrame
    and types of data stored in dataframes columns"""
    print(input_data.head(head))
    column_names = input_data.columns
    for i in column_names:
        print(f"Date type column: {i} {type(input_data[i].iloc[0])}")
    data_shape = input_data.shape
    print(f"csv_data has: {data_shape[0]} rows. {data_shape[1]} columns.")

# Converting JSON to csv file----------------------------------------------------------------------------------------
with open('data/movies_raw_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# name of the movie
movies_titles = [movie["Title"] for movie in data]

# Rating how old people can watch movie
movies_rated = [movie["Rated"] for movie in data]

# Genre of the movies
movies_genre = [movie["Genre"] for movie in data]

# Release date
movies_release = [movie["Released"] for movie in data]
movies_release = [datetime.strptime(date, '%d %b %Y') for date in movies_release]        # Done

# Length of the movies
movies_length = [movie["Runtime"] for movie in data]
movies_length = [int(length.replace(" min", "")) for length in movies_length]            # Done

# Movie director__________________________
movies_director = [movie["Director"] for movie in data]

# Movie writers____________________________
movies_writers = [movie["Writer"] for movie in data]

# Movie actors_____________________________
movies_actors = [movie["Actors"] for movie in data]

movies_language = [movie["Language"] for movie in data]
movies_country = [movie["Country"] for movie in data]

movies_awards = [movie["Awards"] for movie in data]

movies_imdb_rating = [movie["imdbRating"] for movie in data]
movies_imdb_rating = [float(rating) for rating in movies_imdb_rating]                   # Done

movies_imdb_votes = [movie["imdbVotes"] for movie in data]
movies_imdb_votes = [int(vote.replace(',', "")) for vote in movies_imdb_votes]          # Done

movies_imdb_id = [movie["imdbID"] for movie in data]
#
# # Creating data Frame-----------------------------------------------
# data_csv = pd.DataFrame()
# data_csv.index = movies_titles
# data_csv["Released"] = movies_release
# data_csv["Genre"] = movies_genre
# data_csv["Length"] = movies_length
# data_csv["Rating"] = movies_rated
# data_csv["Country"] = movies_country
# data_csv["Language"] = movies_language
# data_csv["Director"] = movies_director
# data_csv["Writers"] = movies_writers
# data_csv["Actors"] = movies_actors
# data_csv["Rewards"] = movies_awards
# data_csv["Imdb_Rating"] = movies_imdb_rating
# data_csv["Imdb_Votes"] = movies_imdb_votes
# data_csv["imdb_ID"] = movies_imdb_id

# budget_and_price = movie_prices(movies_imdb_id)
# data_csv["Movie_Budget"] = budget_and_price[0]
# data_csv["Gross_in_US"] = budget_and_price[1]
# data_csv["World_gross_income"] = budget_and_price[2]
# data_csv["Opening_US_CANADA"] = budget_and_price[3]
# data_csv.to_csv("data/movies_data.csv", index=True)

csv_data = pd.read_csv('data/movies_data.csv')

# Set Unnamed: 0 column as index and renamed it to Titles:
csv_data.set_index(csv_data["Unnamed: 0"], inplace=True)
csv_data.index.name = "Titles:"
csv_data.reset_index(inplace=True)
csv_data.set_index(csv_data["Titles:"], inplace=True)

# Converting str to int in: ["Movie_Budget", "Opening_US_CANADA", "Gross_in_US", "World_gross_income"]
movie_budget = csv_data["Movie_Budget"]
new_budget = []
for price in movie_budget:
    try:
        new_budget.append(int(price))
    except ValueError:
        price = re.findall(r"\d+", price)
        new_budget.append(price)
csv_data["Movie_Budget"] = new_budget

# Creating new column Oscar_Wins with number of wins
raw_rewards = csv_data["Rewards"]

# Oscar/ Oscar nominations
oscar_wins = []
oscar_nomination = []
for reward in raw_rewards:
    sublist = reward.split('.')
    sub_strings = ["Won", "Oscars", "Oscar"]
    sub_string1 = ["Nominated", "Oscar", "Oscars"]

    if all(sublist[0].find(sub_string) != -1 for sub_string in sub_strings):
        wins = re.findall(r'\d+', sublist[0])
        oscar_wins.extend(map(int, wins))  # Convert numbers as integers and append it to list
        oscar_nomination.append(0)
    elif all(sublist[0].find(sub_string) != -1 for sub_string in sub_string1):
        wins = re.findall(r'\d+', sublist[0])
        oscar_nomination.extend(map(int, wins))
        oscar_wins.append(0)
    else:
        oscar_wins.append(0)
        oscar_nomination.append(0)
# --------------------------------------------------------------------

# creating new list with other nominations and wins.
new_nom_wins = []

for reward in raw_rewards:
    sublist = reward.split('.')
    if len(sublist) == 2:
        new_list = sublist[1].split('&')
        new_nom_wins.append(new_list)
    else:
        new_list = sublist[0].split('&')
        if len(new_list) != 2:
            new_list.append("0")
        new_nom_wins.append(new_list)

other_wins = []
other_nominations = []

for i in new_nom_wins:
    if "wins" in i[0]:
        win = re.findall(r'\d+', i[0])
        win = win[0]
        other_wins.append(int(win))
    else:
        other_wins.append(0)
    if "nominations" in i[1]:
        nomination = re.findall(r"\d+", i[1])
        nomination = nomination[0]
        other_nominations.append(int(nomination))
    else:
        other_nominations.append(0)

print(len(new_nom_wins), "/250")
print(f"Wins:\n{other_wins}\n{len(other_wins)}\nNominations: {other_nominations}\n{len(other_nominations)}")

 # Append new columns to DataFrame------------------
csv_data["Oscar_Wins"] = oscar_wins
csv_data["Oscar_Nomination"] = oscar_nomination
csv_data["Other_Wins"] = other_wins
csv_data["Nominations_Total"] = other_nominations

data_type_test(csv_data, head=4)


