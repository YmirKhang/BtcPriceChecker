import urllib
import urllib2
import json
import time
import hmac, hashlib
import config

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

        message = config.key_btcturk + str(int(time.time()))

        sign = hmac.new(hashlib.sha256(config.secret_btcturk.decode('base64').encode('hex')), message  ).hexdigest()
        headers = {
            'X-PCK': config.key_btcturk ,
            'X_Stamp': int(time.time()) ,
            'X-Signature': sign.decode('hex').encode('base64')
        }

        ret = urllib2.urlopen(urllib2.Request('https://www.btcturk.com/api/ticker/balance', headers))
        return  json.loads(ret.read())

b = BtcTurk(APIKey=config.key_btcturk, Secret=config.secret_btcturk)
b.returnBalances()