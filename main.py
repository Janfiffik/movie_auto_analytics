import csv
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

pd.set_option('display.max_columns', None)


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
       its creates JSON file
       You can get your API key by signing in to IMDb database.
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
print(movies_awards)

movies_imdb_rating = [movie["imdbRating"] for movie in data]
movies_imdb_rating = [float(rating) for rating in movies_imdb_rating]                   # Done

movies_imdb_votes = [movie["imdbVotes"] for movie in data]
movies_imdb_votes = [int(vote.replace(',', "")) for vote in movies_imdb_votes]          # Done

# Convert str to int and get rid of 'N/A' value.
movies_cinema_earnings = [movie["BoxOffice"] for movie in data]
movies_cinema_earnings = [earning.replace(',', "") for earning in movies_cinema_earnings]  # Get rid of ','
new_earnings = []                                                                          # New temporary list
for earning in movies_cinema_earnings:
    if earning != 'N/A':
        new_earnings.append(int(earning.replace('$', "")))
    else:
        new_earnings.append(0)
movies_cinema_earnings = new_earnings

data_csv = pd.DataFrame()
data_csv.index = movies_titles
data_csv["Released"] = movies_release
data_csv["Genre"] = movies_genre
data_csv["Length"] = movies_length
data_csv["Rating"] = movies_rated
data_csv["Country"] = movies_country
data_csv["Language"] = movies_language
data_csv["Director"] = movies_director
data_csv["Writers"] = movies_writers
data_csv["Actors"] = movies_actors
data_csv["Rewards"] = movies_awards
data_csv["Imdb_Rating"] = movies_imdb_rating
data_csv["Imdb_Votes"] = movies_imdb_votes
data_csv["Cinema_earnings"] = movies_cinema_earnings

print(data_csv.head(5))
