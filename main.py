from flask import Flask, render_template, request, session

from config import settings
from weather_api.open_meteo import open_meteo_client


app = Flask(__name__)
app.secret_key = settings.app.secret_key

app.template_folder = settings.app.template_folder


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form["city"]
    city_weather = open_meteo_client.get_weather(city)
    return render_template("weather.html", city=city, weather=city_weather)


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
