from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional


class NewMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    released = StringField("Date of release", validators=[DataRequired()])
    genre = SelectField('Movie genre', validators=[DataRequired()],
                        choices=[('Drama', 'Drama'), ( "Crime", 'Crime'), ("Action", 'Action'),
                                 ("Biography", 'Biography'), ("History", 'History'), ("Adventure", "Adventure"),
                                 ("Western", "Western"), ("Sci-Fi", 'Sci-Fi'), ("Fantasy", 'Fantasy'), ("War", 'War'),
                                 ("Animation", 'Animation'), ("Thriller", 'Thriller'), ("Mystery", 'Mystery'),
                                 ("Music", 'Music'), ("Comedy", 'Comedy'), ("Romance", 'Romance'), ("Horror", 'Horror'),
                                 ("Film-Noir", 'Film-Noir')])
    length = IntegerField("Movie length", validators=[DataRequired()])

    Age_Rating = SelectField("Age Rating", validators=[DataRequired()],
                             choices=[("Not rated", 'Not rated'), ('Under 17', 'R'),
                                      ('Parents Guardian under 13', "PG-13"), ("Parents Guardian under 18", 'PG-18'),
                                      ("General audience", 'Approved'), ("Parental Guidance suggested", "PG"),
                                      ("All ages", "G"), ("Television Parental Guidance", "TV-PG"),
                                      ("No one under 17", "X"), ("Television no one under 18", "TV_MA"),
                                      ("Over 18", "+18")])

    country = StringField("Country", validators=[DataRequired()])
    language = StringField("Language", validators=[DataRequired()])
    directors = StringField("Directors", validators=[DataRequired()])
    writers = StringField("Writers", validators=[DataRequired()])
    actors = StringField("Actors", validators=[DataRequired()])
    Imdb_Rating = FloatField("IMDb Rating", validators=[DataRequired()])
    Imdb_Votes = IntegerField("IMDb number of votes", validators=[DataRequired()])
    Imdb_ID = StringField("IMDb ID", validators=[DataRequired()])
    movie_budget = IntegerField("Movie budget", validators=[DataRequired()])
    Gross_US = IntegerField("Gross income in USA", validators=[DataRequired()])
    World_Gross = IntegerField("Gross income in World", validators=[DataRequired()])
    opening_US_CANADA = IntegerField("Income from opening in USA and Canada", validators=[DataRequired()])
    Oscar_Wins = IntegerField("Number of oscars", validators=[DataRequired()])
    Oscar_Nomination = IntegerField("Number oscar nominations", validators=[DataRequired()])
    Other_Wins = IntegerField("Other Wins", validators=[DataRequired()])
    submit = SubmitField("Add movie to DataBase")


class UpdateMovieForm(FlaskForm):
    Imdb_Rating = FloatField("IMDb Rating", validators=[Optional()])
    Imdb_Votes = IntegerField("IMDb number of votes", validators=[Optional()])
    Gross_US = IntegerField("Gross income in USA", validators=[Optional()])
    World_Gross = IntegerField("Gross income in World", validators=[Optional()])
    Oscar_Wins = IntegerField("Number of oscars", validators=[Optional()])
    Oscar_Nomination = IntegerField("Number oscar nominations", validators=[Optional()])
    Other_Wins = IntegerField("Other Wins", validators=[Optional()])
    submit = SubmitField("Update movie in DataBase", validators=[Optional()])
