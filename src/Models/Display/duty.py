from src.common.db import db
from sqlalchemy import or_, and_
from datetime import datetime

class MemberModel(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    member = db.relationship('ServiceMemberModel', backref='member_info')
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)

    def json(self):
        return {'id': self.id,
                'firstName': self.firstname,
                'lastName': self.lastname,
        }

class ServiceMemberModel(db.Model):

    __tablename__ = 'service_member'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def json(self):
        return self.member_info.json()


class DutyModel(db.Model):

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    engine = db.Column(db.String)
    location = db.Column(db.String)
    members = db.relationship('ServiceMemberModel', backref='service')

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
                'location': self.location,
                'members': list(map(lambda x: x.json(), self.members))
                }

    @classmethod
    def get_duty_by_location_engine(cls, location, engine):
        """ Get CIS from database """
        now = datetime.now()

        return cls.query.filter(
            cls.engine == engine,
            cls.location == location
        ).filter(
            or_(
                and_(
                    cls.start < now,
                    cls.end > now
                ),
                cls.start >= now
            )
        ).limit(5)