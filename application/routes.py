import time
from application import app, db
from flask import render_template, flash, request, redirect, url_for, get_flashed_messages
from application.forms import NewMovieForm, UpdateMovieForm
from application.models import MovieDataBase
from datetime import datetime
from application import data_plots as plt


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

        fields_mapping = {'Imdb_Rating': 'Imdb_Rating',
                          'Imdb_Votes': 'Imdb_Votes',
                          'Gross_US': 'Gross_in_Us',
                          'World_Gross': 'World_Gross',
                          'Oscar_Wins': 'Oscar_Wins',
                          'Oscar_Nomination': 'Oscar_Nomination',
                          'Other_Wins': 'Other_Wins'
                          }

        for form_field, db_field in fields_mapping.items():
            form_value = getattr(form, form_field).data
            if form_value:
                setattr(entry, db_field, form_value)

        nomination_total = 0
        if form.Oscar_Wins.data:
            nomination_total += form.Oscar_Wins.data
        else:
            nomination_total += entry.Oscar_Wins

        if form.Oscar_Nomination.data:
            nomination_total += form.Oscar_Nomination.data
        else:
            nomination_total += entry.Oscar_Nomination

        if form.Other_Wins.data:
            nomination_total += form.Other_Wins.data
        else:
            nomination_total += entry.Other_Wins

        entry.Nomination_Total = nomination_total
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


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    MovieDataBase.query.session.close()
    path = "C:/Users/Janokop/PycharmProjects/auto_it_analysis/automatic_analysis/application/instance/moviesDB.db"
    data = plt.raw_pandas_df(path=path)
    data = data.sort_values(by="Imdb_Rating", ascending=False)
    data.loc[:, "Years"] = data["Released"].str[0:4].astype(int)

    rating_vs_budget = plt.group_data(data, ['Title', 'Imdb_Rating', "Movie_Budget"])
    picture = plt.bar_plot(rating_vs_budget, x_col="Title", y_col="Movie_Budget",
                           mk_color="Imdb_Rating", text_column="Imdb_Rating", x_title="",
                           y_title="Movie budget", col_ax_title="Rating", plot_title="")
    rate_vs_budget = picture.to_html(full_html=False)

    rating_vs_date = plt.group_data(data, ['Title', 'Imdb_Rating', 'Released'])
    rating_vs_date = rating_vs_date.sort_values(by="Released", ascending=False)
    picture_2 = plt.bar_plot(rating_vs_date, x_col='Title', y_col="Released",
                             mk_color='Imdb_Rating', text_column="Imdb_Rating", x_title="",
                             y_title="Movie release", col_ax_title="Rating", plot_title="")
    date_of_release_vs_budget = picture_2.to_html(full_html=False)

    years_vs_mean_rating = data[["Years", "Imdb_Rating"]].groupby("Years").mean().reset_index()
    picture_5 = plt.line_plot(years_vs_mean_rating, x_column='Years', y_column='Imdb_Rating', line_shape='Years',
                              mk_color='Years', x_title="Years", y_title="Mean rating",
                              column_ax_title="Average rating by years", plot_title='')
    mean_rating = picture_5.to_html(full_html=False)

    rating_vs_wins = plt.group_data(data, ['Title', 'Imdb_Rating', 'Nomination_Total'])
    picture_3 = plt.bar_plot(rating_vs_wins, x_col='Title', y_col='Nomination_Total', mk_color='Imdb_Rating',
                             text_column='Imdb_Rating', x_title='Nomination_Total', y_title='Nomination_Total',
                             col_ax_title='Imdb_Rating', plot_title='')
    rating_vs_wins = picture_3.to_html(full_html=False)

    new_list = []
    for budget in data["Movie_Budget"]:
        if type(budget) == str:
            budget = budget.replace("[", "").replace("]", "").replace("'", "")
            budget = int(budget) / 1_000_000
            new_list.append(budget)
        else:
            new_list.append(int(budget) / 1_000_000)
    data["Movie_Budget"] = new_list
    data["Gross_Income"] = (data["Gross_in_Us"] + data["World_Gross"] + data["Opening_US_CAN"]) / 1_000_000
    years_vs_budget = data[["Years", "Movie_Budget", "Gross_Income"]].groupby("Years").mean().reset_index()
    years_vs_budget = years_vs_budget.sort_values(by="Years", ascending=True)
    years_vs_budget = years_vs_budget.reset_index()
    picture_4 = plt.line_plot(years_vs_budget, x_column='Years', y_column=['Movie_Budget', 'Gross_Income'],
                              line_shape='Years', mk_color='Years',
                              x_title='Years', y_title='Average Movie Budget in mills',
                              column_ax_title='Movies Budget', plot_title="")
    budget_vs_years = picture_4.to_html(full_html=False)
    best_year = data[data["Years"] == 1977]

    movies_by_country = data[ "Country"].value_counts()
    by_country = plt.pie_plot(data=movies_by_country, values='count', names=movies_by_country.index, title="")
    by_country = by_country.to_html(full_html=False)

    return render_template('dashboard.html', price_vs_rating=rate_vs_budget, date_vs_rating=date_of_release_vs_budget,
                           years_mean_rating=mean_rating, distribution_by_countries=by_country,
                           rating_vs_wins=rating_vs_wins, years_vs_budget=budget_vs_years, best_year=best_year)
