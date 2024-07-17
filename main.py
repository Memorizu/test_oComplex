from flask import Flask, jsonify, render_template, request, session

from config import settings
from weather_api.open_meteo import open_meteo_client


app = Flask(__name__)
app.secret_key = settings.app.secret_key

app.template_folder = settings.app.template_folder


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", last_city=session["last_city"])


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form["city"]

    if "history" not in session:
        session["history"] = []
    session["history"].append(city)
    session["last_city"] = city
    session.modified = True

    city_weather = open_meteo_client.get_weather(city)
    if not city_weather:
        return render_template("404.html", city=city)

    return render_template("weather.html", city=city, weather=city_weather)


@app.route("/stats", methods=["GET"])
def search_stats():
    if "history" not in session:
        session["history"] = []

    search_counts = {}
    for city in session["history"]:
        if city in search_counts:
            search_counts[city] += 1
        else:
            search_counts[city] = 1

    return render_template("stats.html", search_counts=search_counts)


cities = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Нижний Новгород",
    "Казань",
    "Челябинск",
    "Омск",
    "Самара",
    "Ростов-на-Дону",
    "Уфа",
    "Красноярск",
    "Воронеж",
    "Пермь",
]


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")

    suggestions = [city for city in cities if query.lower() in city.lower()]

    return jsonify({"suggestions": suggestions})


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
