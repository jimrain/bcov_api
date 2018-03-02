import requests
import json
import time
import base64
import logging
from bcov_api import BcovUtil

alive_logger = logging.getLogger('alive')


class BcovCMS():
    def __init__(self, accountId, clientId, clientSecret):
        self.bcutil = BcovUtil.BcovUtil(accountId, clientId, clientSecret)
        self.accountId = accountId
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokenTimeout = 0

    # def getAccessToken(self):
    #     current_time = int(time.time())
    #     if current_time > self.tokenTimeout:
    #         oauthUrl = "https://oauth.brightcove.com/v3/access_token"
    #         payload = {'grant_type': 'client_credentials'}
    #         authString = self.clientId + ':' + self.clientSecret
    #         # Little bit of funkiness here. I need to first turn this string into a byte
    #         # array so I can b64 encode it. Then after I encode it I need to turn it
    #         # back in to a string so I can add it to the header.
    #         b_authString = bytes(authString, 'utf-8')
    #         b_array = base64.b64encode(b_authString)
    #
    #         headers = {'Content-Type': 'application/x-www-form-urlencoded',
    #                    'Authorization': 'Basic ' + b_array.decode("utf-8")}
    #         # alive_logger.info(headers)
    #         r = requests.post(oauthUrl, data=payload, headers=headers)
    #         data = r.json()
    #         # Set the timeout to the current time - plus the expiration time - 10 seconds for a buffer.
    #         self.tokenTimeout = current_time + int(data['expires_in']) - 10
    #         # access_token = r.json()['access_token']
    #         self.access_token = data['access_token']
    #
    #     return self.access_token

    def getAccessToken(self):
        return self.bcutil.getAccessToken()

    def getVideoByRefId(self, ref_id):
        # https: // cms.api.brightcove.com / v1 / accounts /:account_id / videos /:video_id
        # Assume it exists until we know other wise.
        exists = True
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/ref:' + ref_id

            r = requests.get(cmsUrl, headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
                exists = False
        except Exception as e:
            alive_logger.error(e.message)
            exists = False

        return exists

    def createVideoWithRefId(self, ref_id):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos'
            data = {
                "name": ref_id,
                "reference_id": ref_id,
            }
            r = requests.post(cmsUrl, data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)

    def deleteVideo(self, video_id):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
        deleteUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id
        r = requests.delete(deleteUrl, data='', headers=headers)
        alive_logger.info(r.status_code)

    def updateVideo(self, ref_id, url):
        s_refId = "ref:" + ref_id
        self.deleteVideo(s_refId)
        self.createVideoWithRefId(ref_id)
        self.addHlsManifest(s_refId, url)

    def addRendition(self, video_id, name, remote_url):
        # https://cms.api.brightcove.com/v1/accounts/:account_id/videos/:video_id/assets/renditions
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            data = {'name': name, 'remote_url': remote_url, 'video_codec': 'h264', 'video_container': 'M2TS'}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id + '/assets/renditions'

            r = requests.post(cmsUrl, data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)

    def updateRendition(self, video_id, name, remote_url, asset_id):
        # https://cms.api.brightcove.com/v1/accounts/:account_id/videos/:video_id/assets/renditions/:asset_id
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            data = {'name': name, 'remote_url': remote_url, 'video_codec': 'h264', 'video_container': 'M2TS',
                    'video_duration': -1}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id + '/assets/renditions/' + asset_id

            r = requests.patch(cmsUrl, data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)

    def getHlsManifestList(self, video_id):
        # https://cms.api.brightcove.com/v1/accounts/:account_id/videos/:video_id/assets/hls_manifest
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id + '/assets/hls_manifest'

            r = requests.get(cmsUrl, headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e.message)

    def addHlsManifest(self, video_id, remote_url):
        # https: // cms.api.brightcove.com / v1 / accounts /:account_id / videos /:video_id / assets / hls_manifest
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            data = {'remote_url': remote_url}
            cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id + '/assets/hls_manifest'

            r = requests.post(cmsUrl, data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e)

    def updateHlsManifest(self, video_id, remote_url, asset_id):
        # https://cms.api.brightcove.com/v1/accounts/:account_id/videos/:video_id/assets/hls_manifest/:asset_id

        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
        # alive_logger.info(headers)
        data = {'remote_url': remote_url}
        cmsUrl = 'https://cms.api.brightcove.com/v1/accounts/' + self.accountId + '/videos/' + video_id + '/assets/hls_manifest/' + asset_id

        r = requests.patch(cmsUrl, data=json.dumps(data), headers=headers)
        if r.status_code == 200 or r.status_code == 201:
            alive_logger.info("HLS Manifests updated")
        else:
            alive_logger.error(r.status_code)
            alive_logger.error(r.text)

    # This is not strictly part of the CMS API but it's the only functionI need out of the player management API
    # so I'm dropping this here.
    def publishPlayer(self, playerId):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            embedURL = 'https://players.api.brightcove.com/v1/accounts/' + self.accountId + '/players/' + playerId + '/publish'
            r = requests.post(embedURL, data="", headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                alive_logger.info(r.json())
            # new_playlist_id = playlist_info['id']
            else:
                alive_logger.error(r.status_code)
                alive_logger.error(r.text)
        except Exception as e:
            alive_logger.error(e)
