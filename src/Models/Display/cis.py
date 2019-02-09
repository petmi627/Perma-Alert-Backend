from .intervention import *
from src.common.db import db

class CisVehicleModel(db.Model):

    __tablename__ = 'cis_vehicle'

    id = db.Column(db.Integer, primary_key=True)
    cis = db.Column(db.Integer)
    vehicle = db.relationship('InterventionEngineModel', backref="vehicle")
    duty = db.Column(db.Integer, db.ForeignKey('cis_engines.id'))
    name = db.Column(db.String)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def get_vehicle_by_name_and_cis(cls, cis, name):
        """ Get CIS from database """
        return cls.query.filter_by(cis=cis, name=name).first()


class CisEngineModel(db.Model):

    __tablename__ = 'cis_engines'

    id = db.Column(db.Integer, primary_key=True)
    cis = db.Column(db.Integer, db.ForeignKey('cis.id'))
    name = db.Column(db.String)
    category = db.Column(db.String)
    duty = db.Column(db.String)
    members = db.Column(db.Integer)
    vehicle = db.relationship('CisVehicleModel')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'duty': self.duty,
            'vehicle': list(map(lambda x: x.json(), self.vehicle))
        }

    @classmethod
    def get_engine_by_name_and_cis(cls, cis, name):
        """ Get CIS from database """
        return cls.query.filter_by(cis=cis, name=name).first()


class CisModel(db.Model):

    __tablename__ = 'cis'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    engines = db.relationship('CisEngineModel')

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def json(self):
        """ Return a directory from Model """
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'engines': list(map(lambda x: x.json(), self.engines))
        }

    @classmethod
    def get_cis_by_location(cls, location):
        """ Get CIS from database """
        return cls.query.filter_by(location=location).first()
