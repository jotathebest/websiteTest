
#!/usr/bin/env python

import sys
import os
import time
import json
import requests
import math
import random
import socket

MAX_TIMEOUT = 10  # In seconds

# UBIDOTS PARAMETERS
URL = "https://things.ubidots.com/api/v1.6/devices"
DEVICE = "uptime-monitor"
VARIABLE = "uptime-check-variable"
HEADERS = {'content-type':'application/json'}
PAYLOAD = json.dumps({"value": 34})

# SLACK PARAMETERS
SLACK_USERNAME = "uptime-robot"
SLACK_CHANNEL = "#uptime_monitor"


def main(token, slack_url):
    try:
        url = "{}/{}/{}/values?token={}".format(URL, DEVICE, VARIABLE, token)
        r = requests.post(url, data=PAYLOAD, headers=HEADERS, timeout= MAX_TIMEOUT)
        if r.status_code != 200 and r.status_code != 201:
            send_alert(slack_url, {r.status_code: r.text})
            return {"status" : "error", "details" : str(r.text)}

        return {"status" : "ok"}

    except Exception as e:
        send_alert(slack_url, {"status" : "error", "details" : str(e)})
        return {"status" : "error", "details" : str(e)}


def send_alert(slack_url, failed_dict):
    try:
        # Alert through Slack
        f_dict = json.dumps(failed_dict, sort_keys=True, indent=4, separators=(',', ': '))
        message = "POST HTTP Outage Alert, see details below\n{}".format(f_dict) 
        slack_dict = {"channel": SLACK_CHANNEL, "username": SLACK_USERNAME, "text": message, "icon_emoji":":ghost:"}
        payload = json.dumps(slack_dict, sort_keys=True, indent=4, separators=(',', ': '))
        r = requests.post(slack_url, data=payload, headers={'content-type':'application/json'}, timeout= 60)
        # Alert through Twilio
    except Exception as e:
        return {'error':'slack post failed'}

if __name__ == "__main__":
    token = os.getenv('TOKEN')
    slack_url = os.getenv('SLACK_URL')
    print(json.dumps(main(token, slack_url)))
