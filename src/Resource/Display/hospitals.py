from bs4 import BeautifulSoup
from flask_restful import Resource, abort
import requests, re

from src.Models.Display.hospital import HospitalModel

class Hospitals(Resource):
    def get(self):

       r = requests.get("http://www.rtl.lu/service/services-de-garde/klinicken")
       if not r.status_code == 200:
           abort(404, message="Cannot get hospital data")

       soup = BeautifulSoup(r.text, "html.parser")

       hospitalList = []

       hospitals = soup.find_all(style=re.compile("background-color: #c6dcc1"))[1:]
       for hospital in hospitals:
           hospitalModel = HospitalModel.get_hospital_by_alias(hospital.b.string)
           hospitalList.append(hospitalModel.json())

       return hospitalList, 200
