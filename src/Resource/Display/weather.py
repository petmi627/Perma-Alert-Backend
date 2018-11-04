from flask_restful import Resource, abort
import requests
from src.Models.Display.cis import CisModel
from src.common.config import Config


class Weather(Resource):

    def transform_weather(self, weather):
        weather = str(weather).replace('light intensity drizzle', 'wi-fog')
        weather = str(weather).replace('drizzle', 'wi-fog')
        weather = str(weather).replace('heavy intensity drizzle', 'wi-fog')
        weather = str(weather).replace('light intensity drizzle rain', 'wi-fog')
        weather = str(weather).replace('drizzle rain', 'wi-fog')
        weather = str(weather).replace('heavy intensity drizzle rain ', 'wi-fog')
        weather = str(weather).replace('shower rain and drizzle', 'wi-fog')
        weather = str(weather).replace('heavy shower rain and drizzle', 'wi-fog')
        weather = str(weather).replace('shower drizzle ', 'wi-fog')
        weather = str(weather).replace('mist', 'wi-fog')
        weather = str(weather).replace('smoke', 'wi-smoke')
        weather = str(weather).replace('haze', 'wi-day-haze')
        weather = str(weather).replace('sand, dust whirls', 'wi-sandstorm')
        weather = str(weather).replace('sand', 'wi-sandstorm')
        weather = str(weather).replace('fog', 'wi-fog')
        weather = str(weather).replace('dust', 'wi-dust')
        weather = str(weather).replace('volcanic ash', 'wi-volcano')
        weather = str(weather).replace('squalls', 'wi-storm-showers')
        weather = str(weather).replace('tornado', 'wi-tornado')
        weather = str(weather).replace('clear sky', 'wi-day-sunny')
        weather = str(weather).replace('few clouds', 'wi-day-cloudy')
        weather = str(weather).replace('scattered clouds', 'wi-cloud')
        weather = str(weather).replace('broken clouds', 'wi-cloudy')
        weather = str(weather).replace('overcast clouds', 'wi-day-sunny-overcast')
        weather = str(weather).replace('light snow', 'wi-snow')
        weather = str(weather).replace('snow', 'wi-snow')
        weather = str(weather).replace('heavy snow', 'wi-snow')
        weather = str(weather).replace('sleet', 'wi-sleet')
        weather = str(weather).replace('shower sleet', 'wi-sleet')
        weather = str(weather).replace('light rain and snow', 'wi-rain-mix')
        weather = str(weather).replace('rain and snow', 'wi-rain-mix')
        weather = str(weather).replace('light shower snow', 'wi-rain-mix')
        weather = str(weather).replace('shower snow', 'wi-rain-mix')
        weather = str(weather).replace('heavy shower snow', 'wi-rain-mix')
        weather = str(weather).replace('light rain', 'wi-rain')
        weather = str(weather).replace('moderate rain', 'wi-rain')
        weather = str(weather).replace('heavy intensity rain', 'wi-rain')
        weather = str(weather).replace('very heavy rain', 'wi-rain')
        weather = str(weather).replace('extreme rain', 'wi-rain')
        weather = str(weather).replace('freezing rain', 'wi-rain')
        weather = str(weather).replace('light intensity shower rain', 'wi-rain')
        weather = str(weather).replace('shower rain', 'wi-rain')
        weather = str(weather).replace('heavy intensity shower rain', 'wi-rain')
        weather = str(weather).replace('ragged shower rain', 'wi-rain')
        weather = str(weather).replace('thunderstorm with light rain', 'wi-thunderstorm')
        weather = str(weather).replace('thunderstorm with heavy rain', 'wi-thunderstorm')
        weather = str(weather).replace('light thunderstorm', 'wi-thunderstorm')
        weather = str(weather).replace('thunderstorm', 'wi-thunderstorm')
        weather = str(weather).replace('heavy thunderstorm', 'wi-thunderstorm')
        weather = str(weather).replace('thunderstorm with light drizzle', 'wi-thunderstorm')
        weather = str(weather).replace('thunderstorm with drizzle', 'wi-thunderstorm')
        weather = str(weather).replace('thunderstorm with heavy drizzle', 'wi-thunderstorm')

        return weather


    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        c = Config()

        request = requests.get('https://api.openweathermap.org/data/2.5/weather?&units=metric&q=' +
                               cis.location + ',LU&appid=' + c.config['secret_keys']['weather_api'])
        if not request.status_code == 200:
            abort(404, message="Cannot get weather data for city {}".format(location))

        weather = request.json()

        print(weather)

        return {
            'temperature': float(weather['main']['temp']),
            'pressure': float(weather['main']['pressure']),
            'humidity': float(weather['main']['humidity']),
            'temp_min': float(weather['main']['temp_min']),
            'temp_max': float(weather['main']['temp_max']),
            'weather': self.transform_weather(weather['weather'][0]['main']),
            'weather_icon': self.transform_weather(weather['weather'][0]['description']),
            'weather_description': str(weather['weather'][0]['description']),
            'wind_speed': weather['wind']['speed'],
            'location': str(weather['name']),
            'country': str(weather['sys']['country']),
        }, 200