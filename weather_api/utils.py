import requests


def get_coordinates_by_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AcmeInc/1.0)",
    }
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
        )

        data = response.json()
        coordinates = {
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
        }
        return coordinates
    except IndexError:
        return None
