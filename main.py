import os
from math import sqrt
import webapp3
import tweepy
import re

auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)


def is_prime(n):
    if n <= 1:
        return False

    if n == 2:
        return True

    for k in range(2, int(sqrt(n))+1):
        if n % k == 0:
            return False

    return True


def is_debug_request(request):
    return request.headers.get('X-Debug-Token') == os.environ['DEBUG_TOKEN']


def is_trusted_requst(request):
    return request.headers.get("X-Appengine-Cron") or is_debug_request(request)

class TweetHandler(webapp3.RequestHandler):
    def get(self):
        global api
        if not is_trusted_requst(self.request):
            self.response.write('not permitted')
            return
        try:
            num = int(re.search(r'(\d+)', list(api.user_timeline(
                screen_name=api.me().screen_name, count=1))[0].text).group(1)) + 1
        except tweepy.TweepError:
            num = 2
        else:
            text = u'%d は素数' % num
            text += u'です' if is_prime(num) else u'ではありません'
            try:
                api.update_status(text)
                self.response.write('tweet successful')
            except tweepy.TweepError:
                self.response.write('tweet failure')


app = webapp3.WSGIApplication([('/tweet', TweetHandler)], debug=True)

if __name__ == '__main__':
    app.run()
