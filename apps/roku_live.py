from bcov_api import BcovLive
from urllib.parse import urlparse
import pickle
import json
import os
import time
import requests

# Live auth tokens.
api_token = 'rvCkWHIDhs4FwUyk2oS0Q7iB9GsXNz5A20UJu1al'
account_id = 'b1eee28922d14ed0b737229dd8cfa457'

# api_token = 'Oiso4rZ4Y9QtwFB0Toeb3ZKVixAOYiI3cIOWCtbf'
# account_id = '5c9b1144ea0a417c993eafecc2375ee9'

slate_url = 'http://solutions.brightcove.com/jrainville/Videos/RokuSlate.mp4'
slate_id = "c9cc8260f202449cb776999915e6a7b2"

abc_slate_url = 'http://solutions.brightcove.com/jrainville/Videos/abc_slate.mp4'
abc_slate_id = '7c43c17a9b474a80bbb8f640b846e2c2'

clipping_creds = 'jrainville-cred'

roku_alive_job_file = "RokuAliveJob.pkl"
roku_ad_config_file = "RokuAdConfig.pkl"
ad_config_archive_file = "Alive_ad_configs.pkl"

# abc_news_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip=OTT_IP&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator=OTT_ADS_TIMESTAMP&scor=OTT_ADS_TIMESTAMP&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre=OTT_CONTENT_GENRE&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"
# people_tv_ad_tag = “https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip={{client.ipaddress}}&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator=OTT_ADS_TIMESTAMP&scor=OTT_ADS_TIMESTAMP&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre={{live.adbreakdurationint}}000&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=ES6dHdJEtK6LO9VW9yON_xgjdPBECu2mgM6aKSJ-Nzc=&roku_cust_param”
abc_news_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip={{client.ipaddress}}&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator={{random.int32}}&scor={{random.int32}}&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre={{live.adbreakdurationint}}000&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"
test_tag = "https://ads.brightcove.com/ads?tech=vast&dur=30&rtid={{rt_id}}"

class RokuLive():

    def __init__(self):
        self.bcov_live = BcovLive.BcovLive(api_token, account_id, clipping_creds)


    def create_ad_configuration(self):
        data = {
            "application_ad_configuration": {
                "ad_configuration_description": "Roku ABC Live Ad Config with duration",
                "ad_configuration_expected_response_type": "Vast",
                "ad_configuration_strategy": "MultipleAdResponse",
                "ad_configuration_transforms": [
                    {
                        "xpath": "/",
                        "xslt": "<xsl:stylesheet version=\"1.0\" xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\" xmlns:Det=\"http://Det.com\"><xsl:output omit-xml-declaration=\"yes\"/><xsl:template match=\"node()|@*\"><xsl:copy><xsl:apply-templates select=\"node()|@*\"/></xsl:copy></xsl:template></xsl:stylesheet>"
                    }],
                "ad_configuration_url_format": abc_news_ad_tag,
            },
            "application_description": "Roku ABC Live ad application with duration",
            "account_id": account_id,
            "application_segment_buffer": 4,
        }

        ad_config = self.bcov_live.create_ad_configuration(data)
        print (ad_config)
        return ad_config


    def create_job(self):
        data = {
            "ad_insertion": True,
            "live_stream": True,
            "static": True,
            "slate": abc_slate_id,
            "region": "us-west-2",
            "reconnect_time": 20,
            "live_sliding_window_duration": 30,
            "ad_audio_loudness_level": -23,
            "add_cdns": [
                {
                    "label": "abcnewslive",
                    "prepend": "abcnewslive.akamaized.net",
                    "protocol": "http",
                    "vendor": "akamai"
                },
            ],
            "notifications": [
                "http://rainville.net:5000/notification",
                {
                    "url": "http://rainville.net:5000/notification",
                    "event": "first_segment_uploaded"
                },
                {
                    "url": "http://rainville.net:5000/notification",
                    "event": "output_finished"
                }],
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


    def press_the_button(self, job_id, duration):
        # job_dict = pickle.load(open(roku_alive_job_file, "rb"))
        # job_id = job_dict['id']

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
        print("RTMP Endpoint: " + job_details['stream_url'])
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

    def get_live_job(self, job_id):

        data = self.bcov_live.get_job(job_id)
        print(json.dumps(data, indent=2))

    def hit_big_red_button_every_10(self, job_id):
        while (True):
            print("Pressing the button...")
            self.press_the_button(job_id, 120)
            time.sleep(600)

    def activate_job_every_10(self, job_id):
        while (True):
            print("Activating Job...")
            self.activate_live_job2(job_id)
            time.sleep(600)

    def test_ad_tag(self):
        test_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip=64.139.253.222&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator=654321&scor=654321&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre=120000&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"

        # alive_logger.info(headers)
        r = requests.get(test_ad_tag)

        print (r.text)
        # data = r.json()

        # print(json.dumps(data, indent=2))


roku = RokuLive()

# job_id = '382de8cf91754c70815b06af58b7ed9e'

job_id = '0765a4a53a0b4a60861e35f0e0b96d24'
application_id =  "125db503b1794886899e5ffa73333d48"

job_id_abc_slate = 'b7a945a127c94926ae33bc7e83315067'
job_id_abc_slate_adjusted_volume = '82d95596697a4bf7933e8eef3da7aaa5'
job_id_abc_cdn = '969431c625e0418ea10b6122b9682af8'


# roku.bcov_live.ingest_slate(abc_slate_url)
# roku.bcov_live.get_assets()

# Step 1 - create the ad config
# roku.create_and_store_ad_config()

# Step 2 - create the live job
# roku.create_and_store_job()

# Step 3 - activate the live job
# roku.activate_live_job()

# Step 4 - Configure the encoder
# roku.dump_rtmp_info()

# Step 5 - Verify Playback
# roku.dump_playback_url()

# Step 6 - Verify ad playback
# roku.press_the_button(job_id, 60)

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

# job_id = '6df8989f8e894a95a1b2d7ce94408630'

# roku.create_ad_configuration()
# '382de8cf91754c70815b06af58b7ed9e'.sep.bcovlive.io:1935/382de8cf91754c70815b06af58b7ed9e
# roku.deactivate_live_job2(job_id)
# roku.activate_live_job2(job_id_abc_slate_adjusted_volume)
# App ID: 6530ce8c27924774bbf8fddd6e9693fa

# roku.get_live_job(job_id)
# roku.dump_ad_config()
# roku.hit_big_red_button_every_10(job_id)

# roku.activate_job_every_10(job_id)

# roku.press_the_button(job_id, 120)

# roku.test_ad_tag()
test_app_id = '1aa2938f028840679887b56c9a22b2cd'
roku.bcov_live.get_ad_configuration(test_app_id)