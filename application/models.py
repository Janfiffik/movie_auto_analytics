from application import db
from datetime import datetime


class MovieDatabase(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    Title: str = db.Column(db.String, nullable=False)
    Released = db.Column(db.DateTime, nullable=False, default="Unknown")
    Genre = db.Column(db.String, nullable=False, default="Genre")
    Length = db.Column(db.Integer, nullable=False, default=0)
    Age_Rating = db.Column(db.String, nullable=False, default="Age_Rating")
    Country = db.Column(db.String, nullable=False, default="Country")
    Language = db.Column(db.String, nullable=False, default="Unknown")
    Director = db.Column(db.String, nullable=False, default="Director")
    Writers = db.Column(db.String, nullable=False, default="Writers")
    Actors = db.Column(db.String, nullable=False, default="actor_name")
    Imdb_Rating = db.Column(db.Integer, nullable=False, default=0)
    Imdb_Votes = db.Column(db.Integer, nullable=False, default=0)
    Movie_Budget = db.Column(db.Integer, nullable=False, default=0)
    Gross_in_Us = db.Column(db.Integer, nullable=False, default=0)
    World_Gross = db.Column(db.Integer, nullable=False, default=0)
    Opening_US_CAN = db.Column(db.Integer, nullable=False, default=0)
    Oscar_Wins = db.Column(db.Integer, nullable=False, default=0)
    Oscar_Nomination = db.Column(db.Integer, nullable=False, default=0)
    Other_Wins = db.Column(db.Integer, nullable=False, default=0)
    Nomination_Total = db.Column(db.Integer, nullable=False, default=0)

    def __str__(self):
        return self.id
