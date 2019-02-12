from InstagramAPI import InstagramAPI
from flask_restful import Resource, abort
from src.common.config import Config
from src.Models.Display.cis import CisModel

class Instagram(Resource):
    def get(self, location):
        cis = CisModel.get_cis_by_location(location=location)
        if not cis:
            abort(404, message="CIS {} doesn't exist".format(location))

        c = Config()

        ig = InstagramAPI(c.config['secret_keys']['instagram_api_user']['username'],
                          c.config['secret_keys']['instagram_api_user']['password'])
        ig.login()

        hashTagList = ['cisdik'] # TODO: Need to get info from database
        personalFeed = []

        for hastag in hashTagList:
            ig.getHashtagFeed(hastag)
            personalFeed.append(ig.LastJson)

        ig.getUserFeed(6009368630) # cgdislux
        feed = ig.LastJson

        d = {
            'personal': personalFeed,
            'main': [feed]
        }

        return d, 200