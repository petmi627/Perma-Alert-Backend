from flask_restful import Resource, abort
from src.Models.Display.cis import CisModel
from flask_jwt_extended import jwt_required, get_jwt_claims

class CIS(Resource):

    @jwt_required
    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if cis:
            claims = get_jwt_claims()
            if not cis.id == claims['cis']['id']:
                abort(403, message="User {} has no access to display.".format(claims['username']))

            return cis.json(), 200
        abort(404, message="CIS {} doesn't exist".format(location))