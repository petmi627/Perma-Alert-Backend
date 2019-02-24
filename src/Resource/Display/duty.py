from flask_restful import Resource, abort
from src.Models.Display.duty import DutyModel
from src.Models.Display.cis import CisModel, CisEngineModel
from flask_jwt_extended import jwt_required

class Duty(Resource):
    @jwt_required
    def get(self, location, engine):
        """ Return a Duty List from specified engine """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        engine = CisEngineModel.get_engine_by_name_and_cis(cis.id, engine)
        if not engine:
            abort(404, message="Engine {} for CIS {} doesn't exist".format(engine, location))

        duties = DutyModel.get_duty_by_location_engine(engine=engine.id, location=cis.id)
        duty_list = list(map(lambda x: x.json(), duties))

        user = {'id': None, 'firstName': None, 'lastName': None}

        for duty in duty_list:
            while len(duty['members']) < engine.members:
                duty['members'].append(user)

        if duty_list:
            return duty_list, 200

        abort(404, message="There are no duties for engine {}".format(engine.name))