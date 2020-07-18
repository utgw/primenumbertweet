# coding: utf-8
from math import sqrt
import webapp3
import tweepy
import re
from key import ckey, csec, atok, asec

auth = tweepy.OAuthHandler(ckey, csec)
auth.set_access_token(atok, asec)
api = tweepy.API(auth)


def isp(n):
    if n <= 1:
        return False

    if n == 2:
        return True

    for k in xrange(2, int(sqrt(n))+1):
        if n % k == 0:
            return False

    return True


def is_trusted_requst(request):
    return request.headers.get("X-Appengine-Cron")

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
            text += u'です' if isp(num) else u'ではありません'
            try:
                api.update_status(text)
                self.response.write('tweet successful')
            except tweepy.TweepError:
                self.response.write('tweet failure')


app = webapp3.WSGIApplication([('/tweet', TweetHandler)], debug=True)

if __name__ == '__main__':
    app.run()
