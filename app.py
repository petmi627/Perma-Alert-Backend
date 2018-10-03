from flask import Flask
from flask_restful import Api
from src.Resource.Display import cis, duty, headlines

app = Flask(__name__)
api = Api(app)

api.add_resource(cis.CIS, '/display/cis/<string:location>')
api.add_resource(duty.Duty, '/display/cis/<string:location>/duties/<string:engine>')
api.add_resource(headlines.Headlines, '/display/headlines')


if __name__ == '__main__':
    app.run(debug=True)

