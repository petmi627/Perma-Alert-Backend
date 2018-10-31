from flask_restful import Resource, abort
from src.Models.Display.duty import DutyModel
from src.Models.Display.cis import CisModel

class Duty(Resource):
    def get(self, location, engine):
        """ Return a Duty List from specified engine """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        duties = DutyModel.get_duty_by_location_engine(engine=engine, location=location)
        duty_list = list(map(lambda x: x.json(), duties))

        user = {'id': None, 'firstName': None, 'lastName': None}
        index = 3
        if engine == 'INC':
            index = 12

        for duty in duty_list:
            while len(duty['members']) < index:
                duty['members'].append(user)

        if duty_list:
            return duty_list, 200

        abort(404, message="There are no duties for engine {}".format(engine))