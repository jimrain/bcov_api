
import requests
import json
import logging

alive_logger = logging.getLogger('alive')

base_url = "https://api.bcovlive.io/v1/"


class BcovLive():
    def __init__(self, api_token, account_id, clipping_creds):
        self.api_token = api_token
        self.account_id = account_id
        self.clipping_creds = clipping_creds

    def create_job(self, data):
        url = base_url + 'jobs/'
        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.post(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)


    def get_job(self, job_id):
        url = base_url + 'jobs/' + job_id

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.get(url, data="", headers=headers)
            status = r.status_code
            if r.status_code == 200:
                alive_logger.info (r.text)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def kill_job(self, job_id):
        cancel_url = base_url + 'jobs/' + job_id + '/cancel'

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.put(cancel_url, data="", headers=headers)
            status = r.status_code
            if r.status_code == 200:
                alive_logger.info (r.text)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def get_assets(self):
        url = base_url + 'ssai/slates/' + self.account_id
        
        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.get(url, headers=headers)
            status = r.status_code
            if r.status_code == 200:
                alive_logger.info(r.text)
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)

    def ingest_slate(self, slate_url):
        url = base_url + 'ssai/slate'
        data = {"source_url": slate_url, "account_id": self.account_id}
        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.post(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def create_ad_configuration(self, data):
        url = base_url + 'ssai/application'

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.post(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def update_ad_configuration(self, app_id, data):
        url = base_url + 'ssai/application/' + app_id

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.put(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def get_ad_configuration(self, app_id):
        url = base_url + 'ssai/application/' + app_id

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}

            r = requests.get(url, headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)

    def big_red_button(self, job_id, duration):
        # "https://api.bcovlive.io/v1/jobs/{jobs_id}/cuepoint
        url = base_url + 'jobs/' + job_id + '/cuepoint'

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}
            data = {"duration": duration}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)
            
    def create_clip(self, job_id, duration, clip_name, vc_creds):
        url = base_url + 'vods'

        try:
            headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_token}
            data = {
                "live_job_id": job_id, 
                "outputs": [
                    {
                    "label": clip_name,
                    "duration": duration,
                    "credentials": vc_creds,
                    "videocloud": {
                        "video": {
                            "name": clip_name
                            },
                        "ingest": {}
                        }
                    }
                ]
                }
            
            r = requests.post(url, data=json.dumps(data), headers=headers)
            status = r.status_code
            if r.status_code == 200:
                j = r.json()
                alive_logger.info(json.dumps(j, indent=2))
                return (j)
            else:
                alive_logger.error (r.status_code)
                alive_logger.error (r.text)
        except Exception as e:
            alive_logger.error (e.message)
            

if __name__ == '__main__':
    alive_logger.error ("Nothing to see here - must be called from a sub class")





