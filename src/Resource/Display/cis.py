from flask_restful import Resource

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
        """ Return a List with cis """
        return cis[cis_name], 200