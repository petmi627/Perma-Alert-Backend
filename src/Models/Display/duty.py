from src.common.db import db
from datetime import datetime

class DutyModel(db.Model):

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    engine = db.Column(db.String)
    location = db.Column(db.String)

    def __init__(self, id, start, end, engine, location):
        self.id = id
        self.start = start
        self.end = end
        self.engine = engine
        self.location = location

    def json(self):
        """ Return a directory from Model """
        return {'id': self.id,
                'start': self.start.isoformat(),
                'end': self.end.isoformat(),
                'engine': self.engine,
                'location': self.location
                }

    @classmethod
    def get_duty_by_location_engine(cls, location, engine):
        """ Get CIS from database """
        now = datetime.now()

        return cls.query.filter(cls.engine == engine, cls.location == location).filter(cls.start >= now).limit(4)