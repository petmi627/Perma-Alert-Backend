from flask_restful import Resource
from src.Models.Display.duty import DutyModel

class Duty(Resource):
    def get(self, location, engine):
        """ Return a Duty List from specified engine """
        return list(map(lambda x: x.json(), DutyModel.get_duty_by_location_engine(engine=engine, location=location))), 200