from flask_restful import Resource, abort
from src.Models.Display.cis import CisModel

class CIS(Resource):

    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if cis:
            return cis.json(), 200
        abort(404, message="CIS {} doesn't exist".format(location))