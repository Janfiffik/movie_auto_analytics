from application import app, db
from flask import render_template, flash, request, redirect, url_for, get_flashed_messages
from application.forms import NewMovieForm, UpdateMovieForm
from application.models import MovieDataBase
from datetime import datetime


@app.route("/")
def index():
    entries = MovieDataBase.query.order_by(MovieDataBase.Imdb_Rating.desc()).all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=["GET", "POST"])
def add_movie():
    form = NewMovieForm()
    if request.method == "POST" and form.validate_on_submit():
        print("submitted", form.data)
        entry = MovieDataBase(Title=form.title.data,
                              Released=datetime.strptime(form.released.data, '%Y-%m-%d'),
                              Genre=form.genre.data,
                              Length=form.length.data,
                              Age_Rating=form.Age_Rating.data,
                              Country=form.country.data,
                              Language=form.language.data,
                              Director=form.directors.data,
                              Writers=form.writers.data,
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
                              Nomination_Total=form.Oscar_Wins.data + form.Oscar_Nomination.data + form.Other_Wins.data
                              )

        db.session.add(entry)
        db.session.commit()
        flash("Successful entry", 'success')
        return redirect(url_for('index'))
    else:
        print("Form validation failed", form.errors)
    return render_template('add.html', title="Add Movie", form=form)


@app.route('/update/<int:movie_id>', methods=["GET", "POST"])
def update_movie(movie_id):
    entry = MovieDataBase.query.get_or_404(int(movie_id))
    form = UpdateMovieForm()
    if request.method == "POST" and form.validate_on_submit():
        entry.Imdb_Rating = form.Imdb_Rating.data
        entry.Imdb_Votes = form.Imdb_Votes.data
        entry.Gross_in_Us = form.Gross_US.data
        entry.World_Gross = form.World_Gross.data
        entry.Oscar_Wins = form.Oscar_Wins.data
        entry.Oscar_Nomination = form.Oscar_Nomination.data
        entry.Other_Wins = form.Other_Wins.data
        entry.Nomination_Total = form.Oscar_Wins.data + form.Oscar_Nomination.data + form.Other_Wins.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("update.html", form=form, old_data=entry)


@app.route('/delete/<int:movie_id>')
def delete_movie(movie_id):
    entry = MovieDataBase.query.get_or_404(int(movie_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Movie was deleted", "success")
    return redirect(url_for("index"))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
