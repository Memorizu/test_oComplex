import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry

from weather_api.utils import get_coordinates_by_city


class OpenMeteoClient:

    __url: str = "https://api.open-meteo.com/v1/forecast"

    __cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    __retry_session = retry(__cache_session, retries=5, backoff_factor=0.2)
    __openmeteo = openmeteo_requests.Client(session=__retry_session)

    def __init__(self, params=None):
        self.params = params
        if not params:
            self.params = {
                "current_weather": "True",
            }

    def get_weather(self, city):
        coordinates = get_coordinates_by_city(city)
        if coordinates:
            self.params.update(coordinates)

        response = requests.get(self.__url, params=self.params)
        return response.json()


def get_weater_client(params=None) -> OpenMeteoClient:
    return OpenMeteoClient(params)


open_meteo_client = get_weater_client()
