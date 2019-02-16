import tweepy
from flask_restful import Resource, abort
from src.common.config import Config
from src.Models.Display.cis import CisModel

class Twitter(Resource):
    def get(self, location):

        c = Config()

        auth = tweepy.OAuthHandler(c.config['secret_keys']['twitter_api_access']['consumer_key'],
                                   c.config['secret_keys']['twitter_api_access']['consumer_secret'])
        auth.set_access_token(c.config['secret_keys']['twitter_api_access']['access_key'],
                              c.config['secret_keys']['twitter_api_access']['access_secret'])
        api = tweepy.API(auth)

        #CGDISlux : 894542671129305088
        tweets_list = []
        user_list = ['894542671129305088']

        for user in user_list:
            feed = tweepy.Cursor(api.user_timeline, id=user).items(7)
            for status in feed:
                tweets_list.append(self.parse_status(api.get_status(status._json['id'], tweet_mode='extended')._json))

        return tweets_list, 200

    def parse_status(self, status):

        d = {
            'id': status['id'],
            'created': status['created_at'],
            'author': {
                'id': status['user']['id'],
                'username': status['user']['screen_name'],
                'full_name': status['user']['name'],
                'avatar': status['user']['profile_image_url_https']
            }
        }

        if 'retweeted_status' in status:
            d['retweet'] = {
                'id': status['retweeted_status']['id'],
                'created': status['retweeted_status']['created_at'],
                'author': {
                    'id': status['retweeted_status']['user']['id'],
                    'username': status['retweeted_status']['user']['screen_name'],
                    'full_name': status['retweeted_status']['user']['name'],
                    'avatar': status['retweeted_status']['user']['profile_image_url_https']
                }
            }
            if 'full_text' in status['retweeted_status']:
                d['retweet']['text'] = status['retweeted_status']['full_text']
            if 'media' in status['retweeted_status']['entities']:
                d['retweet']['images'] = []
                for media in status['retweeted_status']['entities']['media']:
                    if media['type'] == 'photo':
                        d['retweet']['images'].append(media['media_url_https'])
        else:
            d['retweet'] = False
            if 'full_text' in status:
                d['text'] = status['full_text']
            if 'media' in status['entities']:
                d['images'] = []
                for media in status['entities']['media']:
                    if media['type'] == 'photo':
                        d['images'].append(media['media_url_https'])


        return d