from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.forms import NewMovieForm
from application.models import MovieDataBase


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/add', methods=["GET", "POST"])
def add_movie():
    form = NewMovieForm()
    if form.validate_on_submit():
        entry = NewMovieForm(Title=form.title.data,
                             Released=form.released.data,
                             Genre=form.genre.data,
                             Length=form.length.data,
                             Age_Rating=form.Age_Rating.data,
                             Country=form.country.data,
                             Language=form.language.data,
                             Director=form.directors.data,
                             Wrieters=form.writers.data,
                             Actors=form.actors.data,
                             Imdb_Rating=form.Imdb_Rating.data,
                             Imdb_Votes=form.Imdb_Votes.data,
                             Imdb_ID=form.Imdb_ID.data,
                             Movie_Budget=form.movie_budget.data,
                             Gross_in_Us=form.Gross_US.data,
                             World_Gross=form.World_Gross.data,
                             Opening_US_CAN=form.opening_US_CANADA.data,
                             Oscar_Wins=form.Oscar_Wins.data,
                             Oscar_Nomination=form.Oscar_Nomination.data,
                             Other_Wins=form.Other_Wins.data,
                             Nomination_Total=form.Nominations_Total.data
                             )
        db.session.add(entry)
        db.session.commit()
        flash("Successful entry", 'success')
        return redirect(url_for('index'))
    return render_template('add.html', title="add", form=form)
