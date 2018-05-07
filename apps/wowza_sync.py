import requests
import os

from bcov_api import BcovCMS
from bcov_simlive_api import BcovSimLive

# These are global for now, but in reality we can have multiple accounts so these should be kept in a database.
# vc_accountID = "4517911906001"
# vc_clientID = "ea2f0cc2-c6e1-4dce-846c-5ff5ee96910b"
# vc_clientSecret = "2UW_0_uYhuSO0Ka2ew6J6RbkGBC53sEKf49wOuBMv2xQktnJ1zSsbUykv1r8Jz66QGfVe9vGtnme8D8KqZM3IQ"
# Change this to match install
# wowza_root = "/Library/WowzaStreamingEngine/"
wowza_root = "/Users/jim/Downloads/"

class WowzaSync():
    # bcov_cms = BcovCMS.BcovCMS(vc_accountID, vc_clientID, vc_clientSecret)
    bcov_simlive = BcovSimLive.BcovSimLive()

    def write_video_to_storage(self, vid, absolute_video_path, bcov_cms):
        # Strip off existing extension, suck out white space and make it an mp4.
        # name = vid['name'].split('.')[0].replace(" ", "") + '.mp4'
        # print name

        src_url = self.get_high_bit_rate_asset(vid['id'], bcov_cms)

        if src_url is not None:
            try:
                # write the content out to disk.
                r = requests.get(src_url, allow_redirects=True)
                open(absolute_video_path, 'wb').write(r.content)
            except IOError:
                return 'FAILURE'
            return 'SUCCESS'
        else:
            return 'FAILURE'

    def get_high_bit_rate_asset(self, vid_id, bcov_cms):
        assets = bcov_cms.getVideoSources(vid_id)
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

    def get_broadcaststream_vids(self, bcov_cms):
        q = '%2Bbroadcaststream:yes+%2Dbs_sync_status:SUCCESS'
        vids = bcov_cms.getAllVideos(q)
        return vids

    def do_sync(self, bc_account):
        # print (bc_account['accountId'])
        target_dir = wowza_root + 'content/' + bc_account['accountId'] + '/'

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        bcov_cms = BcovCMS.BcovCMS(bc_account['accountId'], bc_account['clientId'], bc_account['clientSecret'])
        vids = self.get_broadcaststream_vids(bcov_cms)
        print (vids)

        for vid in vids:
            # Strip off existing extension, suck out white space and make it an mp4.
            # JR - This doesn't work if there is a period in the title - FIX!
            absolute_video_path = target_dir + vid['name'].split('.')[0].replace(" ", "") + '.mp4'
            print (absolute_video_path)
            status = self.write_video_to_storage(vid, absolute_video_path, bcov_cms)
            print (status)
            if status is 'SUCCESS':
                data = {
                    "name": vid['name'],
                    "bcAccount": bc_account['id'], # This needs to be the pk for the account ID record.
                    "video_id": vid['id'],
                    "duration": vid['duration'],
                    "description": vid['description'],
                    "path": absolute_video_path
                    }
                self.bcov_simlive.create_video(data)

            # print status
            bcov_cms.updateVideo(vid['id'], {"custom_fields": {"bs_sync_status": status}})

    def sync_all_accounts(self):
        bc_accounts = self.bcov_simlive.get_bc_accounts()

        for bc_account in bc_accounts:
            self.do_sync(bc_account)

ws = WowzaSync()
ws.sync_all_accounts()

