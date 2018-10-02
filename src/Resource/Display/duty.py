from flask_restful import Resource

duty = None


class Duty(Resource):

    def get(self, location, engine):
        """ Return a Duty List from specified engine """
        return {'location': location, 'engine': engine}, 200