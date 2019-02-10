from flask_restful import Resource, abort
from bs4 import BeautifulSoup
import requests, re

class Crisis(Resource):
    def get(self):

        r = requests.get("https://www.infocrise.lu/de")
        if not r.status_code == 200:
            abort(404, message="Cannot get crisis data")

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.nav.ul.find_all("li")

        crisis = {}

        for item in items:
            if 'nav--urgence-nucleaire' in item['class']:
                crisis['nuclear'] = self.check_crisis_status('<li class=" nav--urgence-nucleaire ">', item)
            if 'nav--vigilnat' in item['class']:
                crisis['terror'] = self.check_crisis_status('<li class=" nav--vigilnat ">', item)
            if 'nav--intemperies' in item['class']:
                crisis['weather'] = self.check_crisis_status('<li class=" nav--intemperies ">', item)
            if 'nav--ebola' in item['class']:
                crisis['ebola'] = self.check_crisis_status('<li class=" nav--ebola ">', item)
            if 'nav--nombreuse-victimes' in item['class']:
                crisis['mass_casulties'] = self.check_crisis_status('<li class=" nav--nombreuse-victimes ">', item)
            if 'nav--industriel' in item['class']:
                crisis['cbrn'] = self.check_crisis_status('<li class=" nav--industriel ">', item)

        return crisis, 200

    def check_crisis_status(self, to_check, item):
        if to_check in str(item):
            return 'good'
        else:
            return 'alert'
