from application import app
from flask import render_template
from application.forms import NewMovieForm


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/add')
def add_movie():
    form = NewMovieForm()
    return render_template('add.html', title="add", form=form)
