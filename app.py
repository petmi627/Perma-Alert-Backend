from flask import Flask, session
from flask_restful import Api
from flask_cors import CORS
from src.Resource.Display import cis, duty, headlines, intervention, weather, hospitals, calendar, water_levels, crisis, instagram
from src.common.config import Config

config = Config()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.config['database']['localhost']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.config['database']['track_modification']

# Initialize DB
from src.common.db import db
db.init_app(app=app)

api = Api(app)
CORS(app)

api.add_resource(cis.CIS, '/display/cis/<string:location>')
api.add_resource(duty.Duty, '/display/cis/<string:location>/duties/<string:engine>')
api.add_resource(intervention.Intervention, '/display/cis/<string:location>/intervention')
api.add_resource(intervention.InterventionStats, '/display/cis/<string:location>/intervention/<string:vehicle>/stats')
api.add_resource(headlines.Headlines, '/display/headlines')
api.add_resource(hospitals.Hospitals, '/display/hospitals')
api.add_resource(crisis.Crisis, '/display/crisis')
api.add_resource(weather.Weather, '/display/cis/<string:location>/weather')
api.add_resource(weather.Forecast, '/display/cis/<string:location>/weather/forecast')
api.add_resource(water_levels.WaterLevels, '/display/cis/<string:location>/water_level')
api.add_resource(calendar.Calendar, '/display/cis/<string:location>/calendar')
api.add_resource(instagram.Instagram, '/display/cis/<string:location>/instagram')

if __name__ == '__main__':
    app.run(debug=True)

