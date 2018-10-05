from src.common.db import db

class cis(db.Model):

    __tablename__ = 'cis'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)

    def __init__(self, id, name, location, vehicle):
        self.id = id
        self.name = name
        self.location = location
        self.vehicle = vehicle

    def json(self):
        """ Return a directory from Model """
        return {'name': self.name, 'location': self.location, 'vehicle': self.vehicle}

    def get_cis_by_location(self):
        """ Get CIS from database """
