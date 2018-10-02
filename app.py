from flask import Flask
from flask_restful import Api
from src.Resource.Display import cis, duty

app = Flask(__name__)
api = Api(app)

api.add_resource(cis.CIS, '/cis/<string:location>')
api.add_resource(duty.Duty, '/cis/<string:location>/duties/<string:engine>')


if __name__ == '__main__':
    app.run(debug=True)

