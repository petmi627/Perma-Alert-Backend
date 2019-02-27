from flask_restful import Resource, abort
from bs4 import BeautifulSoup
import requests, re
from src.common.config import Config

class Headlines(Resource):
    def get(self):
        c = Config()
        r = requests.get(c.config['url']['headlines'])
        if not r.status_code == 200:
            abort(404, message="Cannot get hospital data")

        rss = BeautifulSoup(r.text, "html.parser")

        headlines = []

        for item in rss.find_all("item"):
            headlines.append({
                'title': item.title.string,
                'description': item.description.string,
                'content': re.sub("<img .*?>", '', item.find("content:encoded").string),
                'link': item.guid.string,
                'media': item.enclosure['url'],
                'published': item.pubdate.string,
                'source': rss.channel.title.string
            })

        return headlines, 200