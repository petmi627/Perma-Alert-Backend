from flask import Flask, session, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.Models.Display import user
from src.Resource.Display import (
    cis,
    duty,
    headlines,
    intervention,
    weather,
    hospitals,
    calendar,
    water_levels,
    crisis,
    instagram,
    twitter,
    user
)
from src.common.config import Config

config = Config()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.config['database']['localhost']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.config['database']['track_modification']
app.secret_key = config.config['secret_keys']['SECRET_KEY']

# Initialize DB
from src.common.db import db
db.init_app(app=app)

api = Api(app)
CORS(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    current_user = user.UserModel.get_user_by_id(identity)
    return current_user.json()

@jwt.expired_token_loader
def expried_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401



api.add_resource(cis.CIS, '/display/cis/<string:location>')
api.add_resource(duty.Duty, '/display/cis/<string:location>/duties/<string:engine>')
api.add_resource(intervention.Intervention, '/display/cis/<string:location>/intervention')
api.add_resource(intervention.InterventionStats, '/display/cis/<string:location>/intervention/<string:engine>/stats')
api.add_resource(headlines.Headlines, '/display/headlines')
api.add_resource(hospitals.Hospitals, '/display/hospitals')
api.add_resource(crisis.Crisis, '/display/crisis')
api.add_resource(weather.Weather, '/display/cis/<string:location>/weather')
api.add_resource(weather.Forecast, '/display/cis/<string:location>/weather/forecast')
api.add_resource(water_levels.WaterLevels, '/display/cis/<string:location>/water_level')
api.add_resource(calendar.Calendar, '/display/cis/<string:location>/calendar')
api.add_resource(instagram.Instagram, '/display/cis/<string:location>/instagram')
api.add_resource(twitter.Twitter, '/display/cis/<string:location>/twitter')
api.add_resource(user.UserLogin, '/login')
api.add_resource(user.TokenRefresh, '/refresh')
api.add_resource(user.UserRegister, '/register')
api.add_resource(user.User, '/users/<string:username>')

if __name__ == '__main__':
    app.run(threaded=True)

