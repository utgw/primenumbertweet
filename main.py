# coding: utf-8
from math import sqrt
import webapp2, tweepy
from key import ckey, csec, atok, asec

auth = tweepy.OAuthHandler(ckey,csec)
auth.set_access_token(atok,asec)
api = tweepy.API(auth)

def isp(n):
  if n == 2: return True
  for k in xrange(2,int(sqrt(n))+1):
    if n%k == 0: return False
  return True

class TweetHandler(webapp2.RequestHandler):
  def get(self):
    global api
    if self.request.headers.get("X-Appengine-Cron"):
      try: num = int(list(api.user_timeline(screen_name=api.me().screen_name, count=1))[0].text) + 1
      except tweepy.TweepError: num = 2
      else:
        try: api.update_status(('%d は素数%s'%(num, 'です' if isp(num) else 'ではありません')).encode())
        except tweepy.TweepError: pass
        finally: break

app = webapp2.WSGIApplication([('/tweet',TweetHandler)],debug=True)

if __name__ == '__main__': app.run()
