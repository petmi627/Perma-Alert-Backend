from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

cis = {
    "diekirch": {
        'name': 'CIS Diekirch',
        'location': 'Diekirch',
        'vehicle': {
            'ambulances': ['AMB1-Diekirch', 'AMB2-Diekirch'],
            'firetrucks': ['DIEKIRCH-HLF21', 'DIEKIRCH-DLK21', 'DIEKIRCH-LF31']
        }
    }
}

class CIS(Resource):
    def get(self, cis_name):
        return cis[cis_name], 200

api.add_resource(CIS, '/cis/<string:cis_name>')


if __name__ == '__main__':
    app.run(debug=True)

