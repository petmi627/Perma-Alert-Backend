from flask_restful import Resource, abort
from src.Models.Display.cis import CisModel
from src.common.config import Config

import datetime
from googleapiclient.discovery import build

class Calendar(Resource):


    def get(self, location):
        """ Return a List with cis """
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        c = Config()
        service = build('calendar', 'v3', developerKey=c.config['secret_keys']['google_api'])

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=c.config['secret_keys']['calendarId'],# Later this info come from the DB
                                              timeMin=now,
                                              maxResults=12,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            abort(404, message="There are no upcoming events in the calendar")

        event_list = []
        for event in events:
            event_list.append({
                "name": event["summary"],
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
                "location": event["location"].split(",")[0]
            })

        return event_list, 200


