from src.common.db import db

class HospitalModel(db.Model):

    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    full_name = db.Column(db.String)
    alias = db.Column(db.String)
    location = db.Column(db.String)
    region = db.Column(db.String)

    def __init__(self, id, name, full_name, alias, location, region):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.alias = alias
        self.location = location
        self.region = region


    def json(self):
        """ Return a directory from Model """
        return {
            'name': self.name,
            'full_name': self.full_name,
            'location': self.location,
            'region': self.region,
        }

    @classmethod
    def get_hospital_by_alias(cls, alias):
        """ Get CIS from database """
        return cls.query.filter_by(alias=alias).first()