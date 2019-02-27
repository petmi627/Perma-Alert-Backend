from flask_restful import Resource, abort
from src.Models.Display.cis import CisModel
from src.common.config import Config

import requests, json


class WaterLevels(Resource):
    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        settings = json.loads(cis.settings)

        c = Config()

        request = requests.get(c.config['url']['water_levels'] + settings['water_station'])
        if not request.status_code == 200:
            abort(404, message="Cannot get water level data for city {}".format(location))

        water_levels = request.json()

        return {
            "city": water_levels['city'],
            "river": water_levels["river"]["name"],
            "trend": water_levels["trend"],
            "current": water_levels["current"],
            "minimum": water_levels["minimum"],
            "maximum": water_levels["maximum"],
            "measurements": water_levels["measurements"],
            "alert_levels": {
                "warn": water_levels["alert_levels"][0],
                "alert": water_levels["alert_levels"][1]
            }
        }, 200
