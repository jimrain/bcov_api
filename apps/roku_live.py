from bcov_api import BcovLive
from urllib.parse import urlparse
import pickle
import json
import os

# Live auth tokens.
api_token = 'rvCkWHIDhs4FwUyk2oS0Q7iB9GsXNz5A20UJu1al'
account_id = 'b1eee28922d14ed0b737229dd8cfa457'

# api_token = 'Oiso4rZ4Y9QtwFB0Toeb3ZKVixAOYiI3cIOWCtbf'
# account_id = '5c9b1144ea0a417c993eafecc2375ee9'

slate_url = 'http://solutions.brightcove.com/jrainville/Videos/RokuSlate.mp4'
slate_id = "c9cc8260f202449cb776999915e6a7b2"

clipping_creds = 'jrainville-cred'

roku_alive_job_file = "RokuAliveJob.pkl"
roku_ad_config_file = "RokuAdConfig.pkl"
ad_config_archive_file = "Alive_ad_configs.pkl"

class RokuLive():

    def __init__(self):
        self.bcov_live = BcovLive.BcovLive(api_token, account_id, clipping_creds)


    def create_ad_configuration(self):
        data = {
            "application_ad_configuration": {
                "ad_configuration_description": "Roku Live Ad Config",
                "ad_configuration_expected_response_type": "Vast",
                "ad_configuration_strategy": "SingleAdResponse",
                "ad_configuration_transforms": [
                    {
                        "xpath": "/",
                        "xslt": "<xsl:stylesheet version=\"1.0\" xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\" xmlns:Det=\"http://Det.com\"><xsl:output omit-xml-declaration=\"yes\"/><xsl:template match=\"node()|@*\"><xsl:copy><xsl:apply-templates select=\"node()|@*\"/></xsl:copy></xsl:template></xsl:stylesheet>"
                    }],
                "ad_configuration_url_format": "https://ads.brightcove.com/ads?tech=vast&dur=30",
            },
            "application_description": "Roku Live ad application",
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
            "slate": slate_id,
            "region": "us-west-2",
            "reconnect_time": 20,
            "live_sliding_window_duration": 30,
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

        print(json.dumps(job_details['ssai_playback_urls'], indent=2))
        print(json.dumps(ad_config, indent=2))

roku = RokuLive()

# roku.create_and_store_ad_config()
# roku.cleanup_ad_configs()
# print (roku.bcov_live.get_account_ad_configurations())

# roku.create_and_store_job()
# print (roku.bcov_live.ingest_slate(slate_url))

roku.press_the_button(60)

# roku.dump_the_pickle()
# roku.dump_rtmp_info()
# roku.dump_ad_config_archive()
# roku.dump_ad_config()
# roku.dump_playback_url()

# roku.kill_live_job()

# print (json.dumps(roku.bcov_live.get_account_ad_configurations(), indent=2))

