from application import db
from datetime import datetime


class MovieDataBase(db.Model):
    __tablename__ = 'movies'
    id: int = db.Column(db.Integer, primary_key=True)
    Title: str = db.Column(db.String, nullable=False)
    Released = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    Genre = db.Column(db.String, nullable=False, default="Genre")
    Length = db.Column(db.Integer, nullable=False, default=0)
    Age_Rating = db.Column(db.String, nullable=True, default="Age_Rating")
    Country = db.Column(db.String, nullable=False, default="Country")
    Language = db.Column(db.String, nullable=False, default="Unknown")
    Director = db.Column(db.String, nullable=False, default="Director")
    Writers = db.Column(db.String, nullable=True)
    Actors = db.Column(db.String, nullable=False, default="actor_name")
    Imdb_Rating = db.Column(db.Integer, nullable=True)
    Roting_Tomato = db.Column(db.Integer, nullable=True)
    Imdb_Votes = db.Column(db.Integer, nullable=True)
    Imdb_ID = db.Column(db.String, nullable=False)
    Movie_Budget = db.Column(db.Integer, default=0)
    Gross_in_Us = db.Column(db.Integer, default=0)
    World_Gross = db.Column(db.Integer, default=0)
    Opening_US_CAN = db.Column(db.Integer, default=0)
    Oscar_Wins = db.Column(db.Integer, default=int(0))
    Oscar_Nomination = db.Column(db.Integer, default=int(0))
    Other_Wins = db.Column(db.Integer, default=int(0))
    Nomination_Total = db.Column(db.Integer, default=int(0))

    def __str__(self):
        return self.id

db.create_all()
