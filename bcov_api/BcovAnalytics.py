import requests
import time
import logging
from bcov_api import BcovUtil

alive_logger = logging.getLogger('alive')


class BcovAnalytics():
    def __init__(self, accountId, clientId, clientSecret):
        self.bcutil = BcovUtil.BcovUtil(accountId, clientId, clientSecret)
        self.accountId = accountId
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokenTimeout = 0

    def getAccessToken(self):
        return self.bcutil.getAccessToken()

    def trackConcurrentUsers(self, ref_id):
        analyticsUrl = "https://analytics.api.brightcove.com/v1/data?accounts=" + self.accountId
        analyticsUrl += "&dimensions=video&fields=video_seconds_viewed"
        analyticsUrl += "&where=video.q==reference_id:" + ref_id
        analyticsUrl += "&reconciled=false"
        analyticsUrl += "&from=-1h&to=now"

        while(1):
            current_time = int(time.time())
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}

            r = requests.get(analyticsUrl, headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                r_headers = r.headers
                for key in r_headers.keys():
                    print (key + " : " + r_headers[key])
                data = r.json()
                # print(data['summary']['video_seconds_viewed'])
                print (data)
            else:
                print(r.status_code)
                print(r.text)
        except Exception as e:
            print(e.message)


# Test harness.
accountId = '4517911906001'
clientId = 'b6cfafb1-46a3-4fad-ab5f-bbef6cfa8a54'
clientSecret = '-AvUg8K1pnXdOwl4HiC46cMFoXngfFU7pSeQqvbVjlqmMz7luLCFzQC9qY1oKShmHP16l5PK8u8QlhlEi-k0Wg'
refId = 'live_analytics_test'

ba = BcovAnalytics(accountId, clientId, clientSecret)

ba.trackConcurrentUsers(refId)
