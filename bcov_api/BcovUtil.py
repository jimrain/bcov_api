import requests
import json
import time
import base64
import logging

alive_logger = logging.getLogger('alive')


class BcovUtil():
    def __init__(self, accountId, clientId, clientSecret):
        self.accountId = accountId
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokenTimeout = 0

    def getAccessToken(self):
        current_time = int(time.time())
        if current_time > self.tokenTimeout:
            oauthUrl = "https://oauth.brightcove.com/v3/access_token"
            payload = {'grant_type': 'client_credentials'}
            authString = self.clientId + ':' + self.clientSecret
            # Little bit of funkiness here. I need to first turn this string into a byte
            # array so I can b64 encode it. Then after I encode it I need to turn it
            # back in to a string so I can add it to the header.
            b_authString = bytes(authString, 'utf-8')
            b_array = base64.b64encode(b_authString)

            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Authorization': 'Basic ' + b_array.decode("utf-8")}
            # alive_logger.info(headers)
            r = requests.post(oauthUrl, data=payload, headers=headers)
            data = r.json()
            # Set the timeout to the current time - plus the expiration time - 10 seconds for a buffer.
            self.tokenTimeout = current_time + int(data['expires_in']) - 10
            # access_token = r.json()['access_token']
            self.access_token = data['access_token']

        return self.access_token
