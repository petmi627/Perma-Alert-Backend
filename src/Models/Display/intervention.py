from src.common.db import db
from datetime import datetime, timedelta

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
    destination_object = db.Column(db.String)
    destination_address = db.Column(db.String)
    destination_region = db.Column(db.String)
    destination_info = db.Column(db.String)
    destination_gps = db.Column(db.String)
    arrival_object = db.Column(db.String)
    arrival_address = db.Column(db.String)
    arrival_region = db.Column(db.String)
    arrival_info = db.Column(db.String)
    arrival_gps = db.Column(db.String)
    alarmed_resources = db.Column(db.String)
    body = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, id , intervention, type, beginning, engione, message, description, caller, ag, cis,
                 destination_object, destination_address, destination_region, destination_info, destination_gps,
                 arrival_object, arrival_address, arrival_region, arrival_info, arrival_gps,
                 alarmed_resources, body, created):
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
        self.destination_object = destination_object
        self.destination_address = destination_address
        self.destination_region = destination_region
        self.destination_info = destination_info
        self.destination_gps = destination_gps
        self.arrival_object = arrival_object
        self.arrival_address = arrival_address
        self.arrival_region = arrival_region
        self.arrival_info = arrival_info
        self.arrival_gps = arrival_gps
        self.alarmed_resources = alarmed_resources
        self.body = body
        self.created = created

    def json(self):
        return {
            'id': self.id,
            'intervention': self.intervention,
            'type': self.type.strip(),
            'beginning': self.beginning.isoformat(),
            'engine': self.engine.split(','),
            'message': self.message,
            'description': self.description,
            'caller': self.caller,
            'ag': self.ag,
            'cis': self.cis,
            'destination': {
                'object': self.destination_object,
                'address': self.destination_address,
                'region': self.destination_region,
                'info': self.destination_info,
                'gps': self.destination_gps
            },
            'arrival': {
                'object': self.arrival_object,
                'address': self.arrival_address,
                'region': self.arrival_region,
                'info': self.arrival_info,
                'gps': self.arrival_gps
            },
            'alarmed_resources': self.sort_alarmed_resources(self.alarmed_resources.split(',')),
            'body': self.body,
            'created': self.created.isoformat(),
        }

    def sort_alarmed_resources(self, resources):
        list = []
        for resource in resources:
            engine = resource.strip().split('(')
            status = resource[resource.find("(")+1:resource.find(")")]
            list.append({'engine': engine[0].strip(), 'status': int(status)})

        return list



    @classmethod
    def get_alarm(cls):
        """ This should return the current intervention """
        now = datetime.now()
        past = now - timedelta(minutes=15)

        return cls.query.filter(cls.created.between(past, now)).first()
