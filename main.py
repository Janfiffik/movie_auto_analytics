import csv
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

pd.set_option('display.max_columns', None)

# # Get movie list and pipeline--------------------------------------------------------------------------------
# Those lines are commented because i don't want to spam IMDB's API
# url_movies = 'https://www.imdb.com/chart/top/'
# headers = {'User-Agent': 'Chrome/58.0.3029.110', 'Accept-Language': 'en-US,en;q=0.9'}
#
# response = requests.get(url_movies, headers=headers)
# movies_names = []
# if response.status_code == 200:
#     raw_data = BeautifulSoup(response.content, 'html.parser')
#     movie_titles = raw_data.find_all(class_='ipc-title-link-wrapper')
#     movies_list = [movie.text for movie in movie_titles]
#     for movie in movies_list[0:250]:
#         movie = (movie.split(' ', 1))
#         movies_names.append(movie[1])
# else:
#     print("Error: ", response.status_code)
# # print(movies_names)  # to check if there are just movie names in list
#
# movies_data = []
# for movie in movies_names:
#     url = 'https://www.omdbapi.com'
#     params = {"plot": "full", "apikey": "<YOUR API KEY FROM IMDB>", "type": "movie", "t": movie}
#
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         movies_data.append(data)
#     else:
#         print("Error: ", response.status_code)

# with open("data/movies_raw_data.json", "w") as file:
#     json.dump(movies_data, file, indent=4, separators=(',', ': '))

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
movies_release = [datetime.strptime(date, '%d %b %Y') for date in movies_release]

# Length of the movies
movies_length = [movie["Runtime"] for movie in data]
movies_length = [int(length.replace(" min", "")) for length in movies_length]

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
movies_imdb_rating = [float(rating) for rating in movies_imdb_rating]

movies_imdb_votes = [movie["imdbVotes"] for movie in data]
movies_imdb_votes = [int(vote.replace(',', "")) for vote in movies_imdb_votes]

movies_cinema_earnings = [movie["BoxOffice"] for movie in data]


# for title in movies_titles:
#     print(title)
# for year in movies_years:
#     print(year)
# for rate in movies_rated:
#     print(rate)
# for genre in movies_genre:
#     print(genre)
# for release in movies_release:
#     print(release)
# for length in movies_length:
#     print(length)
# for director in movies_director:
#     print(director)

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
