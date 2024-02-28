from flask import Flask, render_template
import pandas as pd


def read_data():
    with open("data/movies_data.csv") as file:
        data = pd.read_csv(file)
        return data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    data = read_data()
    movie_names = data["Titles"]
    return render_template("index.html", titles=movie_names)

if __name__ == "__main__":
    app.run(debug=True)
