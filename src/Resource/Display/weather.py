from flask_restful import Resource, abort
import requests
from datetime import datetime, timedelta
from src.Models.Display.cis import CisModel
from src.common.config import Config


class Weather(Resource):

    def transform_weather(self, weather):
        """ Return the Icon name from the Weather Icons Package"""
        c = Config

        icon = str(c.config['weather_icons'][weather['weather'][0]['description'].replace(' ', '_').replace(',', '')])

        sunrise = datetime.fromtimestamp(weather['sys']['sunrise'])
        sunset = datetime.fromtimestamp(weather['sys']['sunset'])
        now = datetime.now()

        icon_format = "night"
        if sunrise < now and sunset > now:
            icon_format = "day"

        if icon_format == "night":
            icon = icon.replace('sunny-overcast', 'partly-cloudy')
            icon = icon.replace('sunny', 'clear')

        return icon.format(icon_format)

    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        c = Config()

        request = requests.get('https://api.openweathermap.org/data/2.5/weather?&units=metric&q=' + # TODO: Get URL from Config
                               cis.location + ',LU&appid=' + c.config['secret_keys']['weather_api'])
        if not request.status_code == 200:
            abort(404, message="Cannot get weather data for city {}".format(location))

        weather = request.json()

        return {
            'temperature': float(weather['main']['temp']),
            'pressure': float(weather['main']['pressure']),
            'humidity': float(weather['main']['humidity']),
            'temp_min': float(weather['main']['temp_min']),
            'temp_max': float(weather['main']['temp_max']),
            'weather': weather['weather'][0]['main'],
            'weather_icon': self.transform_weather(weather),
            'weather_description': str(weather['weather'][0]['description']),
            'wind_speed': weather['wind']['speed'],
            'location': str(weather['name']),
            'country': str(weather['sys']['country']),
            'sunrise': datetime.utcfromtimestamp(weather['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S'),
            'sunset': datetime.utcfromtimestamp(weather['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S'),
        }, 200

class Forecast(Resource):

    def transform_weather(self, weather):
        """ Return the Icon name from the Weather Icons Package"""
        c = Config

        icon = c.config['weather_icons'][weather['weather'][0]['description'].replace(' ', '_').replace(',', '')]
        icon_format = "day"

        return icon.format(icon_format)

    def get(self, location):
        """ Return the Weather Forecast of the given location """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        c = Config()
        request = requests.get('https://api.openweathermap.org/data/2.5/forecast?&units=metric&q=' +
                               cis.location + ',LU&appid=' + c.config['secret_keys']['weather_api'])
        if not request.status_code == 200:
            abort(404, message="Cannot get weather data for city {}".format(location))

        forecast = request.json()
        now = datetime.now()

        forecast_list = []
        for item in forecast['list']:
            dt = datetime.fromtimestamp(item['dt'])
            if dt > now:

                weather = {
                    'temperature': float(item['main']['temp']),
                    'pressure': float(item['main']['pressure']),
                    'humidity': float(item['main']['humidity']),
                    'temp_min': float(item['main']['temp_min']),
                    'temp_max': float(item['main']['temp_max']),
                    'weather': item['weather'][0]['main'],
                    'weather_icon': self.transform_weather(item),
                    'weather_description': str(item['weather'][0]['description']),
                    'wind_speed': item['wind']['speed'],
                    'location': str(forecast['city']['name']),
                    'country': str(forecast['city']['country']),
                    'datetime': dt.isoformat()
                }

                forecast_list.append(weather)
                now += timedelta(days=1)


        return forecast_list, 200
