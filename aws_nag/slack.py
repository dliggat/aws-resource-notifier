import json
import logging
from urllib2 import Request, urlopen, URLError, HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Slack(object):

    def __init__(self, channel=None, username='AWS Nag', url=None, text=None):

        self.message = {
            'channel': channel,
            'username': username,
            'text': text,
            'icon_emoji': ':timer_clock:'
        }
        self.url = url

    def invoke(self):
        req = Request(self.url, json.dumps(self.message))
        try:
            response = urlopen(req)
            response.read()
            logger.info("Message posted to %s", self.message['channel'])

        except HTTPError as e:
            logger.error("Request failed: %d %s", e.code, e.reason)
        except URLError as e:
            logger.error("Server connection failed: %s", e.reason)
