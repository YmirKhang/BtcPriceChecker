import urllib
import urllib2
import json
import time
from hmac import new as hmac
import hashlib
import config
import base64

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class BtcTurk:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if ('return' in after):
            if (isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if (isinstance(after['return'][x], dict)):
                        if ('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))

        return after

    def returnBalances(self):
        signature = self.authSignature()
        headers = {
            "X-PCK": self.APIKey ,
            "X-Stamp": str(int(time.time())) ,
            "X-Signature": signature
        }

        try:
            ret = urllib2.urlopen(urllib2.Request('https://www.btcturk.com/api/balance', headers=headers))
        except urllib2.HTTPError as e:
            print e.code
            print e.read()
        return  json.loads(ret.read())

    def authSignature(self):
        unixTime = int(time.time())

        message = self.APIKey + str(unixTime)

        temp= hmac(base64.b64decode(self.Secret), message, hashlib.sha256).digest()
        return base64.b64encode(temp)


print int(time.time())
b= BtcTurk(APIKey=config.key_btcturk,Secret=config.secret_btcturk)
print b.returnBalances()
