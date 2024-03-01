from application import db


class MovieDatabase(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    Title: str = db.Column(db.String, nullable=False)
    Released = db.Column(db.Datetime)
    Genre = db.Column(db.String)
    Length = db.Column(db.Integer)
    Age_Rating = db.Column(db.String)
    Country = db.Column(db.String)
    Writers = db.Column(db.String)
    Actors = db.Column(db.String)
    Imdb_Rating = db.Column(db.Integer)
    Imdb_Votes = db.Column(db.Integer)
    Movie_Budget = db.Column(db.Integer)
    Gross_in_Us = db.Column(db.Integer)
    World_Gross = db.Column(db.Integer)
    Opening_US_CAN = db.Column(db.Integer)
    Oscar_Wins = db.Column(db.Integer)
    Oscar_Nomination = db.Column(db.Integer)
    Other_Wins = db.Column(db.Integer)
    Other_Nomination = db.Column(db.Integer)

