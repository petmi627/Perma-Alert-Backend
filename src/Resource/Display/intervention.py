from flask_restful import Resource, abort
from src.common.config import Config
from src.Models.Display.cis import CisModel, CisVehicleModel
from src.Models.Display.intervention import InterventionModel

class Intervention(Resource):
    def get(self, location):
        c = Config()
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))
        alarm = InterventionModel.get_alarm(cis.id, api_key=c.config['secret_keys']['google_maps_key'])
        if not alarm:
            abort(404, message="No Intervention found now, for CIS {}".format(cis.location))

        return alarm.json(), 200

class InterventionStats(Resource):
    def get(self, location, vehicle):
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        vehicle = CisVehicleModel.get_vehicle_by_name_and_cis(cis.id, vehicle)
        if not vehicle:
            abort(404, message="Vehicle {} for CIS {} doesn't exist".format(vehicle, location))

        stats = InterventionModel.get_stats_by_vehicle(cis, vehicle)

        return stats, 200