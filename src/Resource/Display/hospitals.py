from bs4 import BeautifulSoup
from flask_restful import Resource, abort
import requests, re, datetime
from src.common.config import Config

from src.Models.Display.hospital import HospitalModel

class Hospitals(Resource):
    def get(self):
       c = Config()
       r = requests.get(c.config['url']['hospitals'])
       if not r.status_code == 200:
           abort(404, message="Cannot get hospital data")

       soup = BeautifulSoup(r.text, "html.parser")

       now = datetime.datetime.now()
       start = datetime.datetime.now().replace(hour=7)
       end = datetime.datetime.now().replace(hour=19)

       hospitalList = []

       hospitals = soup.find_all(style=re.compile("background-color: #c6dcc1"))[1:]
       for hospital in hospitals:

           hospital_name = hospital.b.string

           hospitals = hospital.find_all("b")
           if len(hospitals) > 1:
               for item in hospitals:
                   if item.next_sibling == "de 7.00 à 19.00 hrs" and start < now and end > now:
                       hospital_name = item.string
                       break

                   hospital_name = item.string

           hospitalModel = HospitalModel.get_hospital_by_alias(hospital_name)
           if hospitalModel:
                hospitalList.append(hospitalModel.json())

       return hospitalList, 200
