from flask_restful import Resource, abort

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

    def abort_if_cis_doesnt_exist(self, location):
        if location not in cis:
            abort(404, message="CIS {} doesn't exist".format(location))

    def get(self, location):
        """ Return a List with cis """
        self.abort_if_cis_doesnt_exist(location)
        return cis[location], 200