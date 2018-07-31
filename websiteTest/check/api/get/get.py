import os
import json
import requests
import socket

MAX_TIMEOUT = 10  # In seconds

# UBIDOTS PARAMETERS
URL = "https://things.ubidots.com/api/v1.6/devices"
DEVICE = "uptime-monitor"
VARIABLE = "get"

# SLACK PARAMETERS
SLACK_USERNAME = "uptime-robot"
SLACK_CHANNEL = "#uptime_monitor"

def main(token, slack_url):
    try:
        url = "{}/{}/{}/?token={}".format(URL, DEVICE, VARIABLE, token)
        r = requests.get(url, timeout= MAX_TIMEOUT)
        if r.status_code != 200 and r.status_code != 201:
            send_alert(slack_url, {r.status_code: r.text})
            return {"status" : "error", "details" : r.text}

        value = r.json()['last_value']['value']

        if  int(value) != 1:
            failed_dict = {"505" : "value retrieved should be 1 not {}".format(value)}
            send_alert(slack_url, failed_dict)
            return {"status" : "error", "details" : "value retrieved should be 1 not {}".format(value)}

        return {"status" : "ok"}

    except Exception as e:
        failed_dict = {"status" : "error", "details" : str(e)}
        send_alert(slack_url, failed_dict)
        return {"status" : "error", "details" : str(e)}


def send_alert(slack_url, failed_dict):
    try:
        # Alert through Slack
        f_dict = json.dumps(failed_dict, sort_keys=True, indent=4, separators=(',', ': '))
        message = "GET HTTP Outage Alert, see details below\n{}".format(f_dict) 
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