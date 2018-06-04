from bcov_api import BcovLive
from urllib.parse import urlparse
import pickle
import json
import os

# Live auth tokens.
api_token = 'Vn1SxBe5Ka1jwkJMbnjMsauxMu7xsjKkahAuzFe4'
account_id = '34c415e261504306ab42793e92408f89'

clipping_creds = 'jrainville-cred'

roku_alive_job_file = "RokuAliveJob.pkl"
roku_ad_config_file = "RokuAdConfig.pkl"
ad_config_archive_file = "Alive_ad_configs.pkl"

# abc_news_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip=OTT_IP&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator=OTT_ADS_TIMESTAMP&scor=OTT_ADS_TIMESTAMP&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre=OTT_CONTENT_GENRE&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"
abc_news_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip={{client.ipaddress}}&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator={{random.int32}}&scor={{random.int32}}&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre=OTT_CONTENT_GENRE&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"
test_tag = "https://ads.brightcove.com/ads?tech=vast&dur=30&rtid={{rt_id}}"

class PeopleTVLive():

    def __init__(self):
        self.bcov_live = BcovLive.BcovLive(api_token, account_id, clipping_creds)


    def create_ad_configuration(self):
        data = {
            "application_ad_configuration": {
                "ad_configuration_description": "Roku ABC Live Ad Config",
                "ad_configuration_expected_response_type": "Vast",
                "ad_configuration_strategy": "SingleAdResponse",
                "ad_configuration_transforms": [
                    {
                        "xpath": "/",
                        "xslt": "<xsl:stylesheet version=\"1.0\" xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\" xmlns:Det=\"http://Det.com\"><xsl:output omit-xml-declaration=\"yes\"/><xsl:template match=\"node()|@*\"><xsl:copy><xsl:apply-templates select=\"node()|@*\"/></xsl:copy></xsl:template></xsl:stylesheet>"
                    }],
                "ad_configuration_url_format": abc_news_ad_tag,
            },
            "application_description": "Roku ABC Live ad application",
            "account_id": account_id,
            "application_segment_buffer": 4
        }

        ad_config = self.bcov_live.create_ad_configuration(data)
        print (ad_config)
        return ad_config


    def create_job(self):
        data = {
            "ad_insertion": True,
            "live_stream": True,
            "static": True,
            "region": "us-west-2",
            "reconnect_time": 20,
            "live_sliding_window_duration": 30,

            "outputs": [
                {
                    "label": "hls720p",
                    "live_stream": True,
                    "width": 960,
                    "height": 540,
                    "video_codec": "h264",
                    "h264_profile": "main",
                    "video_bitrate": 1843,
                    "segment_seconds": 6,
                    "keyframe_interval": 60
                },
                {
                    "label": "hls480p",
                    "live_stream": True,
                    "width": 640,
                    "height": 360,
                    "video_codec": "h264",
                    "h264_profile": "main",
                    "video_bitrate": 819,
                    "segment_seconds": 6,
                    "keyframe_interval": 60
                }
            ]
        }

        return self.bcov_live.create_job(data)


    def create_and_store_job(self):
        job_details = self.create_job()
        print(json.dumps(job_details, indent=2))
        pickle.dump(job_details, open(roku_alive_job_file, "wb"))

    def activate_live_job(self):
        job = pickle.load(open(roku_alive_job_file, "rb"))
        job_id = job['id']
        self.bcov_live.acitvate_sep_stream(job_id)

    def activate_live_job2(self, job_id):
        self.bcov_live.acitvate_sep_stream(job_id)

    def deactivate_live_job(self):
        job = pickle.load(open(roku_alive_job_file, "rb"))
        job_id = job['id']
        self.bcov_live.deacitvate_sep_stream(job_id)

    def deactivate_live_job2(self, job_id):
        self.bcov_live.deacitvate_sep_stream(job_id)

    def create_and_store_ad_config(self):
        ad_config = self.create_ad_configuration()
        print(json.dumps(ad_config, indent=2))
        pickle.dump(ad_config, open(ad_config_archive_file, "wb"))

    def cleanup_ad_configs(self):
        configs = self.bcov_live.get_account_ad_configurations()
        # Pickle the configs in case I need them later.
        # pickle.dump(configs, open("Alive_ad_configs.pkl", "wb"))
        for config in configs:
            print(self.bcov_live.delete_ad_configuration(config['application_id']))

    def kill_live_job(self):
        job_dict = pickle.load(open(roku_alive_job_file, "rb"))
        job_id = job_dict['id']
        self.bcov_live.kill_job(job_id)
        # Remove the pickle file so we don't save stale data
        os.remove(roku_alive_job_file)


    def press_the_button(self, duration):
        job_dict = pickle.load(open(roku_alive_job_file, "rb"))
        job_id = job_dict['id']

        self.bcov_live.big_red_button(job_id, duration)


    def dump_ad_config_archive(self):
        ad_configs = pickle.load(open(ad_config_archive_file, "rb"))
        print(json.dumps(ad_configs, indent=2))

    def dump_the_pickle(self):
        job_details = pickle.load(open(roku_alive_job_file, "rb"))
        print(json.dumps(job_details, indent=2))

    def dump_rtmp_info(self):
        job_details = pickle.load(open(roku_alive_job_file, "rb"))
        print ("Application Name: " + job_details['id'])
        stream_info = urlparse(job_details['stream_url'])
        print ("Host: " + stream_info.netloc.split(':')[0])
        print("Stream Name: " + job_details['stream_name'])

    def dump_ad_config(self):
        ad_config = pickle.load(open(ad_config_archive_file, "rb"))
        print(json.dumps(ad_config, indent=2))

    def dump_playback_url(self):
        job_details = pickle.load(open(roku_alive_job_file, "rb"))
        ad_config = pickle.load(open(ad_config_archive_file, "rb"))

        app_id = ad_config['application']['application_id']
        ssai_url = job_details['ssai_playback_urls'][app_id]['playback_url']

        print("SSAI Playback URL: " + ssai_url)

    def get_job(self, job_id):
        job_details = self.bcov_live.get_job(job_id)
        print(json.dumps(job_details, indent=2))

ptv = PeopleTVLive()

# job_id = "90dcf390063d411ba84c0bd18fc06330"
         # /us-east-1/5755101710001/b1fd4a8527534d158bba12282529a7e4/playlist_ssaiM.m3u8
job_id = '94e17775a2864be0a8997e0a7f2a7db0'
# ptv.deactivate_live_job2(job_id)
# ptv.activate_live_job2(job_id)
ptv.get_job(job_id)

# Step 1 - create the ad config
# roku.create_and_store_ad_config()

# Step 2 - create the live job
# ptv.create_and_store_job()

# Step 3 - activate the live job
# ptv.activate_live_job()

# Step 4 - Configure the encoder
# roku.dump_rtmp_info()

# Step 5 - Verify Playback
# roku.dump_playback_url()

# Step 6 - Verify ad playback
# roku.press_the_button(60)

# Step 7 - deactivate the live job
# roku.deactivate_live_job()

# Step 8 - Kill the live job (optional)
# roku.kill_live_job()

# Misc - utilities
# print (roku.bcov_live.ingest_slate(slate_url))

# roku.cleanup_ad_configs()
# print (roku.bcov_live.get_account_ad_configurations())

# print (json.dumps(roku.bcov_live.get_account_ad_configurations(), indent=2))
# roku.dump_the_pickle()
