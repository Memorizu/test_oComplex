from flask.testing import FlaskClient
import requests_mock

from weather_api.utils import get_coordinates_by_city


def test_get_lat_lon():
    with requests_mock.Mocker() as m:
        city = "Kazan"
        latitude = 55.7887
        longitude = 49.1221
        m.get(
            f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1",
            json=[{"lat": latitude, "lon": longitude}],
        )

        coordinates = get_coordinates_by_city(city)
        assert coordinates == {"latitude": latitude, "longitude": longitude}


def test_index_page(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 200


def test_weather_page(client: FlaskClient):
    with requests_mock.Mocker() as m:
        city = "Kazan"
        latitude = 55.7887
        longitude = 49.1221
        m.get(
            f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1",
            json=[{"lat": latitude, "lon": longitude}],
        )
        m.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true",
            json={"current_weather": {"temperature": 20}},
        )

        response = client.post("/weather", data={"city": city})
        assert response.status_code == 200
