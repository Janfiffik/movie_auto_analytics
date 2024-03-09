from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import random
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time as tm
import re
from application import app, db
from application.models import MovieDataBase

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def save_data_to_database(data_to_db):
    """Function for sawing pandas DataFrame to file.db
       data_to_db: it accepts Pandas dataframe """
    for _, row in data_to_db.iterrows():
        try:
            release_time = datetime.strptime(str(row["Released"]), '%Y-%m-%d')
        except ValueError:
            release_time = None
        entry = MovieDataBase(Title=row["Titles"],
                              Released=release_time,
                              Genre=row["Genre"],
                              Length=row["Length"],
                              Age_Rating=row["Rating"],
                              Country=row["Country"],
                              Language=row["Language"],
                              Director=row["Director"],
                              Writers=row["Writers"],
                              Actors=row["Actors"],
                              Imdb_Rating=row["Imdb_Rating"],
                              Roting_Tomato=row["Roting_Tomato"],
                              Imdb_Votes=row["Imdb_Votes"],
                              Imdb_ID=row["imdb_ID"],
                              Movie_Budget=row["Movie_Budget"],
                              Gross_in_Us=row["Gross_in_US"],
                              World_Gross=row["World_gross_income"],
                              Opening_US_CAN=row["Opening_US_CANADA"],
                              Oscar_Wins=row["Oscar_Wins"],
                              Oscar_Nomination=row["Oscar_Nomination"],
                              Other_Wins=row["Other_Wins"],
                              Nomination_Total=row["Oscar_Wins"] + row["Oscar_Nomination"] + row["Other_Wins"]
                              )

        db.session.add(entry)
        db.session.commit()


def if_in_data(title):
    entry = MovieDataBase.query.get_or_404(title)
    db.session.commit()
    print(entry.data)


def imdb_movies():
    """For getting movie list from imdb database by webscraping"""
    page = 1
    movies_names = []
    for j in range(8):
        url_movies = f'https://www.imdb.com/list/ls000634294/' \
                     f'?sort=list_order,asc&st_dt=&mode=simple&page={page}&ref_=ttls_vw_smp'
        headers = {'User-Agent': 'Chrome/58.0.3029.110', 'Accept-Language': 'en-US,en;q=0.9'}

        response = requests.get(url_movies, headers=headers)
        if response.status_code == 200:
            raw_data = BeautifulSoup(response.content, 'html.parser')
            movie_titles = raw_data.find_all(class_='lister-item-header')
            movies_list = [movie.text for movie in movie_titles]

            pattern0 = r'\d+\.\s+(.*?)\s+\(\d{4}(?:–\d{4})?\)'
            pattern1 = r'\d+\.\s+(.*?)\s+\(\d{4}.*?\)'
            pattern2 = r'\d+\.\s+([A-Za-z0-9\s]+?)\s+\(\d{4}(?:–\d{4})?\)'
            pattern3 = r'\d+\.\s+(.*?)\s+\(\d{4}\)'
            pattern4 = r'\d+\.\s+(.*?)\s+\(.*?\d{4}(?:–\d{4})?\)'
            for movie in movies_list:
                match = re.search(pattern0, movie)
                match1 = re.search(pattern1, movie)
                match2 = re.search(pattern2, movie)
                match3 = re.search(pattern3, movie)
                match4 = re.search(pattern4, movie)
                if match:
                    movie_name = match.group(1)
                    movies_names.append(movie_name)
                elif match1:
                    movie_name = match1.group(1)
                    movies_names.append(movie_name)
                elif match2:
                    movie_name = match2.group(1)
                    movies_names.append(movie_name)
                elif match3:
                    movie_name = match3.group(1)
                    movies_names.append(movie_name)
                elif match4:
                    movie_name = match4.group(1)
                    movies_names.append(movie_name)
            page += 1
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
            print("Success")
        else:
            print("Error: ", response.status_code)
        tm.sleep(random.choice(range(0, 1)))
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


def data_type_test(input_data, head=5, data_type=False):
    """Prints first 5 rows from DataFrame
       and types of data stored in dataframes columns.

       It accepts argument head=integer
       to pick how many lines from DataFrame should be printed in terminal

       Argument data_type=True prints data type in each column in DataFrame.
    """
    print(f"{input_data.head(head)}\n")
    column_names = input_data.columns
    if data_type:
        for j in column_names:
            print(f"Date type column: {j} {type(input_data[j].iloc[0])}")
    data_shape = input_data.shape
    print(f"csv_data has: {data_shape[0]} rows. {data_shape[1]} columns.")


# Code automation-----------------------------------------------------------------------------------------------


def schedule_yearly():
    """Function for returning how many seconds lef to the 1 january of the next year"""
    now = datetime.now()
    current_year = now.year
    next_year = current_year + 1
    next_year_date = datetime(next_year, 1, 1, 0, 0, 0)
    time_remaining = next_year_date - now
    time_remaining_seconds = time_remaining.total_seconds()
    return time_remaining_seconds


# While loop
while True:
    time_left = schedule_yearly()
    tm.sleep(1)
    if time_left > 1:
        # print(f"waiting: {time_left}")
        continue
    else:
        # Converting JSON to file.db file---------------------------------------------------------------
        movie_names = imdb_movies()
        movie_json_data(movie_names, api_key="<YOUR API KEY>")

with open('data/movies_raw_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
movies_titles = [movie["Title"] for movie in data]         # name of the movie
movies_rated = [movie["Rated"] for movie in data]          # Rating how old people can watch movie
movies_genre = [movie["Genre"] for movie in data]          # Genre of the movies

movies_release = [movie["Released"] for movie in data]     # Release date
movies_release = [datetime.strptime(date, '%d %b %Y') if date != 'N/A' else None for date in movies_release]

movies_length = [movie["Runtime"] for movie in data]      # Length of the movies
movies_length = [int(length.replace(" min", "")) for length in movies_length]

movies_director = [movie["Director"] for movie in data]
movies_writers = [movie["Writer"] for movie in data]
movies_actors = [movie["Actors"] for movie in data]
movies_language = [movie["Language"] for movie in data]

movies_country = [movie["Country"] for movie in data]
movies_awards = [movie["Awards"] for movie in data]
movies_imdb_rating = [movie["imdbRating"] for movie in data]

movies_roten_tomato = []
for movie in data:
    try:
        if movie["Ratings"][1]["Source"] == "Rotten Tomatoes":
            movie = movie["Ratings"][1]["Value"]
            movies_roten_tomato.append(movie)
        else:
            movies_roten_tomato.append(None)
    except IndexError:
        movies_roten_tomato.append(None)

        movies_roten_tomato = [rating.replace("%", "") if rating is not None else None for rating in movies_roten_tomato]
        movies_imdb_rating = [float(rating) if rating != 'N/A' else None for rating in movies_imdb_rating]
        movies_imdb_votes = [movie["imdbVotes"] for movie in data]

        movies_imdb_votes = [int(vote.replace(',', "")) if vote != 'N/A' else None for vote in movies_imdb_votes]
        movies_imdb_id = [movie["imdbID"] for movie in data]

        # Creating data_base -----------------------------------------------

        csv_data = pd.DataFrame()
        csv_data["Titles"] = movies_titles
        csv_data["Released"] = movies_release
        csv_data["Genre"] = movies_genre
        csv_data["Length"] = movies_length
        csv_data["Rating"] = movies_rated
        csv_data["Country"] = movies_country
        csv_data["Language"] = movies_language
        csv_data["Director"] = movies_director
        csv_data["Writers"] = movies_writers
        csv_data["Actors"] = movies_actors
        csv_data["Rewards"] = movies_awards
        csv_data["Imdb_Rating"] = movies_imdb_rating
        csv_data["Roting_Tomato"] = movies_roten_tomato
        csv_data["Imdb_Votes"] = movies_imdb_votes
        csv_data["imdb_ID"] = movies_imdb_id

        budget_and_price = movie_prices(movies_imdb_id)
        csv_data["Movie_Budget"] = budget_and_price[0]
        csv_data["Gross_in_US"] = budget_and_price[1]
        csv_data["World_gross_income"] = budget_and_price[2]
        csv_data["Opening_US_CANADA"] = budget_and_price[3]

        # Set Titles column as index---------------------------------------------------------
        csv_data.reset_index(inplace=True)
        csv_data.set_index(csv_data["Titles"], inplace=True)

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

        # Creating new column Oscar_Wins with number of wins--------------------------------------------------
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

        for i in new_nom_wins:
            if "wins" in i[0]:
                win = re.findall(r'\d+', i[0])
                win = win[0]
                other_wins.append(int(win))
            else:
                other_wins.append(0)

        # Append new columns to DataFrame------------------
        csv_data["Oscar_Wins"] = oscar_wins
        csv_data["Oscar_Nomination"] = oscar_nomination
        csv_data["Other_Wins"] = other_wins

        # Deleting useless columns------------------------------
        del csv_data["Rewards"]
        del csv_data["index"]

        csv_data.to_csv("data/movie_data.csv", index=False)

        # Write updated DataFrame to DataBase
        save_data_to_database(data_to_db=csv_data)
        continue


