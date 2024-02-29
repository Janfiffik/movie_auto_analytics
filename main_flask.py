import base64
from flask import Flask, render_template
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt


def plot_frame(data, kind="line", size=(9, 9), **kwargs):
    """
       Plots the given DataFrame.

       Parameters
       :param data: DataFrame, the data to be plotted.
       :param kind: str, optional (default='line'). The kind of plot to draw: 'line', 'bar', 'hist', 'box', 'scatter',
                                                                              'area', 'barh', 'kde', 'density, 'hexbin',
                                                                              'pie'.
       :param size: Accepts a tuple with two numbers optional: default(9, 9).
       : **kwargs: Additional keyword arguments to be passed to the plot function.
       :return:
       -BytesIO: BytesIO object containing the plot image.
    """
    plt.figure(figsize=size)
    data.plot(kind=kind, **kwargs)
    plt.xticks(rotation=45)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return img_buffer


def read_data():
    with open("data/movies_data.csv") as file:
        data = pd.read_csv(file)
        return data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    data = read_data()
    price_oscar = data[["Movie_Budget", "Oscar_Wins"]]
    img_price_oscar = plot_frame(price_oscar, kind='line', size=(8, 6),
                                 title="Oscar wins vs. budget", xlabel="Budget",
                                 ylabel="Oscar wins")
    img_data = base64.b64encode(img_price_oscar.getvalue()).decode('utf-8')
    return render_template("index.html", img_data=img_data)

if __name__ == "__main__":
    app.run(debug=True)
