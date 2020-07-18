import os
from math import sqrt
from flask import Flask, request
import tweepy
import re

app = Flask(__name__)

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


def is_debug_request(req):
    return req.headers.get('X-Debug-Token') == os.environ['DEBUG_TOKEN']


def is_trusted_requst(req):
    return req.headers.get("X-Appengine-Cron") or is_debug_request(req)

@app.route('/tweet')
def tweet():
    global api
    if not is_trusted_requst(request):
        return 'not permitted', 403
    try:
        num = int(re.search(r'(\d+)', list(api.user_timeline(
            screen_name=api.me().screen_name, count=1))[0].text).group(1)) + 1
    except tweepy.TweepError:
        num = 2
    else:
        text = '%d は素数' % num
        text += 'です' if is_prime(num) else 'ではありません'
        try:
            api.update_status(text)
            return 'tweet successful'
        except tweepy.TweepError:
            return 'tweet failure', 500


if __name__ == '__main__':
    app.run()
