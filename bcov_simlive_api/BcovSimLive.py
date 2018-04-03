import requests
import json
import time
import base64
import logging
from bcov_api import BcovUtil

alive_logger = logging.getLogger('alive')

base_simlive_url = 'http://localhost:8000/simlive/'


class BcovSimLive():
    def __init__(self):
        print ("BcovSimLiveApi init.")

    def create_video(self, video_data):
        headers = {'Content-Type': 'application/json'}

        # data = {
        #     "title": "Test Title",
        #     "bcAccount": "1", # This needs to be the pk for the account ID record.
        #     "video_id": "12345",
        #     "duration": "23",
        #     "description": "This is my first video",
        #     "path": "path to the video"
        #     }

        videoUrl = base_simlive_url + 'videos'
        r = requests.post(videoUrl, data=json.dumps(video_data), headers=headers)

        return (r.status_code)

    def get_bc_accounts(self):
        account_url = base_simlive_url + 'accounts'
        r = requests.get(account_url)

        if r.status_code >= 200 and r.status_code < 300:
            return r.json()
        else:
            return None

    def apiTest(self):
        print (self.get_bc_accounts())

# bcSimLive = BcovSimLive()
# bcSimLive.apiTest()