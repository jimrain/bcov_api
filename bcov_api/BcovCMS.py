import requests
import json
import time
import base64
import logging
from bcov_api import BcovUtil

alive_logger = logging.getLogger('alive')

base_cms_url = 'https://cms.api.brightcove.com/v1/accounts/'

class BcovCMS():
    def __init__(self, accountId, clientId, clientSecret):
        self.bcutil = BcovUtil.BcovUtil(accountId, clientId, clientSecret)
        self.accountId = accountId
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokenTimeout = 0


    def getAccessToken(self):
        return self.bcutil.getAccessToken()

    def getAllVideos(self, q=None):
        step = 25
        offset = 0
        done = False
        videos = []

        total_vids = 0

        while not done:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            # print(headers)
            getVidsUrl = base_cms_url + str(self.accountId) + '/videos?limit=25&offset=' + str(offset)
            if q is not None:
                getVidsUrl += ('&q=' + q)

            # print getVidsUrl

            offset += step
            r = requests.get(getVidsUrl, data='', headers=headers)
            # print r.status_code
            if r.status_code == 200:
                video_info = r.json()
                if not video_info:
                    done = True
                    # print ("Done")
                else:
                    total_vids = total_vids + len(video_info)
                    # print ("Total vids: " + str(total_vids))
                    for video in video_info:
                        videos.append(video)
            else:
                print r.status_code
                print r.text

        return videos


    def getVideoSources(self, video_id):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
        getSourcesListUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/sources'
        r = requests.get(getSourcesListUrl, data='', headers=headers)
        video_sources = r.json()
        return video_sources


    def updateVideo(self, video_id, video_data):
        createVidUrl = base_cms_url + self.accountId + '/videos/' + video_id
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
        r = requests.patch(createVidUrl, data=json.dumps(video_data), headers=headers)
        video_info = r.json()
        # print json.dumps(video_info, sort_keys=True, indent=4, separators=(',', ': '))

        if r.status_code >= 200 and r.status_code < 300:
            vid = r.json()
            return (video_info)
        else:
            print r.status_code
            print r.text
            return None


    def getVideoByRefId(self, ref_id):
        # https: // cms.api.brightcove.com / v1 / accounts /:account_id / videos /:video_id
        # Assume it exists until we know other wise.
        exists = True
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            cmsUrl = base_cms_url + self.accountId + '/videos/ref:' + ref_id

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
            cmsUrl = base_cms_url + self.accountId + '/videos'
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
        deleteUrl = base_cms_url + self.accountId + '/videos/' + video_id
        r = requests.delete(deleteUrl, data='', headers=headers)
        alive_logger.info(r.status_code)

    def updateVideo_manifest(self, ref_id, url):
        s_refId = "ref:" + ref_id
        self.deleteVideo(s_refId)
        self.createVideoWithRefId(ref_id)
        self.addHlsManifest(s_refId, url)

    def addRendition(self, video_id, name, remote_url):
        # https://cms.api.brightcove.com/v1/accounts/:account_id/videos/:video_id/assets/renditions
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.getAccessToken()}
            data = {'name': name, 'remote_url': remote_url, 'video_codec': 'h264', 'video_container': 'M2TS'}
            cmsUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/assets/renditions'

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
            cmsUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/assets/renditions/' + asset_id

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
            cmsUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/assets/hls_manifest'

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
            cmsUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/assets/hls_manifest'

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
        cmsUrl = base_cms_url + self.accountId + '/videos/' + video_id + '/assets/hls_manifest/' + asset_id

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
