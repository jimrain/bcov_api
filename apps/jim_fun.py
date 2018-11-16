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

clipping_creds = 'jrainville-cred'

test_tag = "https://ads.brightcove.com/ads?tech=vast&dur=30&rtid={{rt_id}}"

class JimFun():

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


    def press_the_button(self, job_id, duration):
        # job_dict = pickle.load(open(roku_alive_job_file, "rb"))
        # job_id = job_dict['id']

        self.bcov_live.big_red_button(job_id, duration)


    def dump_ad_config_archive(self):
        ad_configs = pickle.load(open(ad_config_archive_file, "rb"))
        print(json.dumps(ad_configs, indent=2))


    def get_live_job(self, job_id):

        data = self.bcov_live.get_job(job_id)
        print(json.dumps(data, indent=2))

    def hit_big_red_button_every_10(self, job_id):
        while (True):
            print("Pressing the button...")
            self.press_the_button(job_id, 120)
            time.sleep(600)

    def test_ad_tag(self):
        test_ad_tag = "https://ravm.tv/ads?version=1.0&inv_type=rr&sz=1920x1080&ssai_req=1&ip=64.139.253.222&coppa=OTT_ADS_KIDS_CONTENT&min_ad_duration=0&max_ad_duration=60000&is_raf=1&is_roku=1&rdid=ROKU_ADS_TRACKING_ID&ottid=OTT_ADS_TRACKING_ID&is_lat=OTT_ADS_LIMIT_TRACKING&is_roku_lat=ROKU_ADS_LIMIT_TRACKING&idtype=OTT_ID_TYPE&correlator=654321&scor=654321&pod=POD_NUM&ppos=POD_POSITION&ad_vertical=OTT_AD_VERTICAL&ad_roll=AD_ROLL&genre=120000&content=OTT_CONTENT_ID&length=OTT_CONTENT_LENGTH&device=OTT_DEVICE_MODEL&ua=OTT_USER_AGENT&ai=ROKU_ADS_APP_ID&ott_app_id=OTT_ADS_APP_ID&fb_url=&rtid=iZxSwaTKoSX9_EL3JX4zN_gEghuxbi4zq_NwOnIMJA4=&roku_cust_param"

        # alive_logger.info(headers)
        r = requests.get(test_ad_tag)

        print (r.text)
        # data = r.json()

        # print(json.dumps(data, indent=2))

    def insert_id3_tag(self, job_id):
        print(job_id)
        id3_tag = {
            "id3_tag": {
                "name": "oON",
                "value": "overlay_on",
            }
        }
        self.bcov_live.insert_id3_tag(job_id, id3_tag)


fun = JimFun()

job_id = '14ea91e8226349728e5ea5e5cd88298d'
fun.insert_id3_tag(job_id)

