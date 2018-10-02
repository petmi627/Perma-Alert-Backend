from flask import Flask
from flask_restful import Api
from src.Resource.Display import cis

app = Flask(__name__)
api = Api(app)

api.add_resource(cis.CIS, '/cis/<string:cis_name>')


if __name__ == '__main__':
    app.run(debug=True)

