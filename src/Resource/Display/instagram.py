from InstagramAPI import InstagramAPI
from flask_restful import Resource, abort
from src.common.config import Config
from src.Models.Display.cis import CisModel
import datetime

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

        feed = None

        for hastag in hashTagList:
            ig.getHashtagFeed(hastag)
            feed = self.parse_json(ig.LastJson)

        userFeedList = ['6009368630'] #cgdislux
        for user in userFeedList:
            ig.getUserFeed(user)
            feed = self.parse_json(ig.LastJson, feed)

        return feed, 200

    def parse_json(self, feed, list=[]):
        for post in feed['items']:
                d = {
                    'id': post['id'],
                    'created': datetime.datetime.utcfromtimestamp(post['taken_at']).strftime('%Y-%m-%d %H:%M:%S'),
                    'likes': post['like_count'],
                    'comments': post['comment_count'],
                    'author': {
                        'id': post['user']['pk'],
                        'username': post['user']['username'],
                        'full_name': post['user']['full_name'],
                        'avatar': post['user']['profile_pic_url']
                    }
                }

                if 'image_versions2' in post:
                    d['image'] = [post['image_versions2']['candidates'][0]['url']]
                elif 'carousel_media' in post:
                    d['image'] = []
                    for image in post['carousel_media']:
                        d['image'].append(image['image_versions2']['candidates'][0]['url'])
                else:
                    continue


                if 'caption' in post:
                    d['caption'] = post['caption']['text']

                if 'location' in post:
                    d['location'] = post['location']['name']

                if 'preview_comments' in post:
                    d['comments_preview'] = []
                    for comment in post['preview_comments']:
                        dc = {
                            'id': comment['pk'],
                            'created': datetime.datetime.utcfromtimestamp(comment['created_at_utc']).strftime(
                                '%Y-%m-%d %H:%M:%S'),
                            'text': comment['text'],
                            'author': {
                                'id': comment['user']['pk'],
                                'username': comment['user']['username'],
                                'full_name': comment['user']['full_name'],
                                'avatar': comment['user']['profile_pic_url']
                            },
                        }

                        d['comments_preview'].append(dc)

                list.append(d)

        return list