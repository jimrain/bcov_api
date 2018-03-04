import requests
import os

from bcov_api import BcovCMS

# These are global for now, but in reality we can have multiple accounts so these should be kept in a database.
vc_accountID = "4517911906001"
vc_clientID = "ea2f0cc2-c6e1-4dce-846c-5ff5ee96910b"
vc_clientSecret = "2UW_0_uYhuSO0Ka2ew6J6RbkGBC53sEKf49wOuBMv2xQktnJ1zSsbUykv1r8Jz66QGfVe9vGtnme8D8KqZM3IQ"
# Change this to match install
wowza_root = "/Library/WowzaStreamingEngine/"

class WowzaSync():
    bcov_cms = BcovCMS.BcovCMS(vc_accountID, vc_clientID, vc_clientSecret)

    def write_video_to_storage(self, vid, target_dir):
        # Strip off existing extension, suck out white space and make it an mp4.
        name = vid['name'].split('.')[0].replace(" ", "") + '.mp4'
        # print name

        src_url = self.get_high_bit_rate_asset(vid['id'])

        if src_url is not None:
            try:
                # write the content out to disk.
                r = requests.get(src_url, allow_redirects=True)
                open(target_dir + name, 'wb').write(r.content)
            except IOError:
                return 'FAILURE'
            return 'SUCCESS'
        else:
            return 'FAILURE'

    def get_high_bit_rate_asset(self, vid_id):
        assets = self.bcov_cms.getVideoSources(vid_id)
        high_bit_rate = 0

        # src_url =  self.bcAcctAnalyzer.getDigitalMasterPath(vid)
        # print src_url
        src_url = None

        for asset in assets:
            try:
                if asset['container'] == "MP4":
                    if asset['encoding_rate'] > high_bit_rate:
                        high_bit_rate = asset['encoding_rate']
                        src_url = asset['src']
            except KeyError:
                continue

        return src_url

    def get_broadcaststream_vids(self):
        q = '%2Bbroadcaststream:yes+%2Dbs_sync_status:SUCCESS'
        vids = self.bcov_cms.getAllVideos(q)
        return vids

    def do_sync(self):
        target_dir = wowza_root + 'content/' + vc_accountID + '/'

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        vids = self.get_broadcaststream_vids()

        for vid in vids:
            status = self.write_video_to_storage(vid, target_dir)
            # print status
            self.bcov_cms.updateVideo(vid['id'], {"custom_fields": {"bs_sync_status": status}})


ws = WowzaSync()
ws.do_sync()

