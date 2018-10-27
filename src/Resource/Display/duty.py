from flask_restful import Resource, abort
from src.Models.Display.duty import DutyModel

class Duty(Resource):
    def get(self, location, engine):
        """ Return a Duty List from specified engine """

        duties = DutyModel.get_duty_by_location_engine(engine=engine, location=location)

        print(duties)

        duty_list = list(map(lambda x: x.json(), duties))

        if duty_list:
            return duty_list, 200
        abort(404, message="There are no duties for engine {}".format(engine))