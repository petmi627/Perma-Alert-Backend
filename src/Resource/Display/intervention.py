from flask_restful import Resource, abort
from src.Models.Display.cis import CisModel
from src.Models.Display.intervention import InterventionModel

class Intervention(Resource):
    def get(self, location):
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))
        alarm = InterventionModel.get_alarm()
        if not alarm:
            abort(404, message="No Intervention found now, for CIS {}".format(location))

        return alarm.json(), 200