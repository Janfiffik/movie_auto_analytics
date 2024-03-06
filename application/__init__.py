from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Janokop/PycharmProjects/auto_it_analysis/' \
                                        'automatic_analysis/application/instance/moviesDB.db'

app.config['SECRET_KEY'] = "fdgdfgn;dfbdngfmfgksmnbsrtihnmmsnbksbsnfgjnhbd"

db = SQLAlchemy(app)

from application import routes
