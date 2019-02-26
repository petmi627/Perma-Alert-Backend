from flask_restful import Resource, abort
from src.common.config import Config
from src.Models.Display.cis import CisModel, CisVehicleModel, CisEngineModel
from src.Models.Display.intervention import InterventionModel
from flask_jwt_extended import jwt_required, get_jwt_claims

class Intervention(Resource):
    @jwt_required
    def get(self, location):
        c = Config()
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))
        claims = get_jwt_claims()
        if not cis.id == claims['cis']['id']:
            abort(403, message="User {} has no access to display.".format(claims['username']))
        alarm = InterventionModel.get_alarm(cis.id, api_key=c.config['secret_keys']['google_maps_key'])
        if not alarm:
            abort(404, message="No Intervention found now, for CIS {}".format(cis.location))

        return alarm.json(), 200

class InterventionStats(Resource):
    @jwt_required
    def get(self, location, engine):
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        claims = get_jwt_claims()
        if not cis.id == claims['cis']['id']:
            abort(403, message="User {} has no access to display.".format(claims['username']))

        engine = CisEngineModel.get_engine_by_name_and_cis(cis.id, engine)
        if not engine:
            abort(404, message="Engine {} for CIS {} doesn't exist".format(engine, location))

        vehicle = CisVehicleModel.get_vehicle_by_engine(engine.id)
        if not vehicle:
            abort(404, message="Vehicle {} for CIS {} doesn't exist".format(vehicle, location))

        stats = InterventionModel.get_stats_by_vehicle(cis, vehicle)

        return stats, 200