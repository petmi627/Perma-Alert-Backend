from .cis import *
from src.common.db import db
from datetime import datetime, timedelta
import calendar


class InterventionModel(db.Model):

    __tablename__ = 'intervention'

    id = db.Column(db.Integer, primary_key=True)
    intervention = db.Column(db.Integer)
    type = db.Column(db.String)
    beginning = db.Column(db.DateTime)
    engine = db.Column(db.String)
    message = db.Column(db.String)
    description = db.Column(db.String)
    caller = db.Column(db.String)
    ag = db.Column(db.Boolean)
    cis = db.Column(db.String)
    vehicles = db.relationship('InterventionEngineModel', backref='intervention_info')
    destination = db.Column(db.Integer, db.ForeignKey('intervention_address_destination.id'))
    destination_complete = db.relationship('InterventionDestinationModel', back_populates="intervention")
    destination_info = db.Column(db.String)
    arrival = db.Column(db.Integer, db.ForeignKey('intervention_address_arrival.id'))
    arrival_complete = db.relationship('InterventionArrivalModel', back_populates="intervention")
    arrival_info = db.Column(db.String)
    alarmed_resources = db.Column(db.String)
    body = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, id , intervention, type, beginning, engione, message, description, caller, ag, cis,
                 destination_info, arrival_info, alarmed_resources, body, created):
        self.id = id
        self.intervention = intervention
        self.type = type
        self.beginning = beginning
        self.engine = engione
        self.message = message
        self.description = description
        self.caller = caller
        self.ag = ag
        self.cis = cis
        self.destination_info = destination_info
        self.arrival_info = arrival_info
        self.alarmed_resources = alarmed_resources
        self.body = body
        self.created = created

    def json(self):
        return {
            'id': self.id,
            'intervention': self.intervention,
            'type': self.type.strip(),
            'beginning': self.beginning.isoformat(),
            'engine': list(map(lambda x: x.json(), self.vehicles)),
            'message': self.message,
            'description': self.description,
            'caller': self.caller,
            'ag': self.ag,
            'cis': self.cis,
            'destination': self.check_address(self.destination_complete.json()),
            'destination_info': self.destination_info,
            'destination_map': self.get_map(self.destination_complete),
            'arrival': self.check_address(self.arrival_complete),
            'arrival_info': self.arrival_info,
            'arrival_map': self.get_map(self.arrival_complete),
            'alarmed_resources': self.sort_alarmed_resources(self.alarmed_resources.split(',')),
            'body': self.body,
            'created': self.created.isoformat(),
        }

    def check_address(self, address):
        if address == None:
            return None

        return address

    def sort_alarmed_resources(self, resources):
        list = []
        for resource in resources:
            engine = resource.strip().split('(')
            status = resource[resource.find("(")+1:resource.find(")")]
            list.append({'engine': engine[0].strip(), 'status': status})

        return list

    def get_map(self, destination):
        if not destination:
            return None

        base = 'https://www.google.com/maps/embed/v1/place?key=' + self.api_key
        if destination.postal or destination.street:
            url = base + "&q=" + destination.street + ", " + str(destination.postal) + " " + str(destination.city)
        elif destination.street:
            url = base + "&q=" + destination.street + ", " + str(destination.city)
        else:
            url = base + "&q=" + str(destination.city)

        return url

    @classmethod
    def get_alarm(cls, cis, api_key):
        """ This should return the current intervention """
        cls.api_key = api_key
        now = datetime.now()
        past = now - timedelta(minutes=15)

        return cls.query.filter(cls.created.between(past, now)).filter_by(cis=cis).first()

    @classmethod
    def get_stats_by_vehicle(cls, cis, vehicle):
        now = datetime.now()

        # Get Last Intervention
        last_intervention = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.cis == cis.id
        ).order_by(cls.id.desc()).first()

        # Get Intervention Today
        start = now.strftime('%Y-%m-%d') + " 00:00:00"
        end = now.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_today = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).count()

        yesterday = now - timedelta(days=1)
        start = yesterday.strftime('%Y-%m-%d') + " 00:00:00"
        end = yesterday.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_yesterday = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=6)
        start = start.strftime('%Y-%m-%d') + " 00:00:00"
        end = end.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_this_week = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        start = now - timedelta(days=now.weekday(), weeks=1)
        end = start + timedelta(days=6)
        start = start.strftime('%Y-%m-%d') + " 00:00:00"
        end = end.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_last_week = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        start = now.strftime('%Y-%m-') + "01 00:00:00"
        end = now.replace(day=calendar.monthrange(now.year, now.month)[1])
        end = end.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_this_month = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        start = now.replace(day=1)
        start_dt = start - timedelta(days=1)
        start = start_dt.strftime('%Y-%m-') + "01 00:00:00"
        end = start_dt.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_last_month = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        start = now.replace(day=1, month=1)
        start = start.strftime('%Y-%m-%d') + " 00:00:00"
        end = now.replace(day=31, month=12)
        end = end.strftime('%Y-%m-%d') + " 23:59:59"
        interventions_this_year = cls.query.join(cls.vehicles).filter(
            InterventionEngineModel.engine == vehicle.id, cls.created.between(start, end), cls.cis == cis.id).order_by(
            cls.id.desc()).count()

        return {
               'last_intervention': str(last_intervention.beginning),
               'stats_timeline': {
                   'interventions_today': int(interventions_today),
                   'interventions_yesterday': int(interventions_yesterday),
                   'interventions_this_week': int(interventions_this_week),
                   'interventions_last_week': int(interventions_last_week),
                   'interventions_this_month': int(interventions_this_month),
                   'interventions_last_month': int(interventions_last_month),
                   'intervention_this_year': int(interventions_this_year)
                }
        }


class InterventionEngineModel(db.Model):
    __tablename__ = 'intervention_engine'

    id = db.Column(db.Integer, primary_key=True)
    intervention = db.Column(db.Integer, db.ForeignKey('intervention.id'))
    engine = db.Column(db.Integer, db.ForeignKey('cis_vehicle.id'))

    def json(self):
        return self.vehicle.json()


class InterventionArrivalModel(db.Model):
    __tablename__ = 'intervention_address_arrival'

    id = db.Column(db.Integer, primary_key=True)
    intervention = db.relationship("InterventionModel", back_populates="arrival_complete")
    object = db.Column(db.String)
    street = db.Column(db.String)
    postal = db.Column(db.Integer)
    city = db.Column(db.String)
    region = db.Column(db.String)
    longitude = db.Column(db.String)
    latitude = db.Column(db.String)

    def json(self):
        return {'id': self.id,
                'object': self.object,
                'street': self.street,
                'postal': self.postal,
                'city': self.city,
                'region': self.region,
                'longitude': self.longitude,
                'latitude': self.latitude
                }


class InterventionDestinationModel(db.Model):
    __tablename__ = 'intervention_address_destination'

    id = db.Column(db.Integer, primary_key=True)
    intervention = db.relationship("InterventionModel", back_populates="destination_complete")
    object = db.Column(db.String)
    street = db.Column(db.String)
    postal = db.Column(db.Integer)
    city = db.Column(db.String)
    region = db.Column(db.String)
    longitude = db.Column(db.String)
    latitude = db.Column(db.String)

    def json(self):
        return {'id': self.id,
                'object': self.object,
                'street': self.street,
                'postal': self.postal,
                'city': self.city,
                'region': self.region,
                'longitude': self.longitude,
                'latitude': self.latitude
                }
