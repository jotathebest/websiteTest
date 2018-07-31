from boto3.session import Session
import numpy as np
import cv2
from PIL import Image
import io
import base64
import random
import sys
import json
import requests


# SLACK PARAMETERS
SLACK_USERNAME = "uptime-robot"
SLACK_CHANNEL = "#uptime_monitor"


def compare_images(template, testing, delta=0):
    '''
    @template: Template image
    @testing: Testing image (actual screenshot)
    @delta: Max percentage of difference in pixels
    '''
    if template is None or testing is None:
        print("[ERROR] Could not read properly the images")
        return True

    if template.shape != testing.shape:
        print("[ERROR] Images do not have the same shape")
        return True

    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    testing_gray = cv2.cvtColor(testing, cv2.COLOR_RGB2GRAY)

    xor = np.bitwise_xor(template_gray, testing_gray)
    ones = cv2.countNonZero(xor)
    pixels = template.shape[1] * template.shape[0]

    # If there is at least the same delta difference, the images are different
    result = (ones / pixels) > (delta / 100.0)

    return result


def send_to_s3(img, aws_access_key_id, aws_secret_access_key, aws_bucket_data):
    '''
    Sends and store an image in AWS
    @img must be a numpy array
    '''
    try:
        import StringIO
    except:
        from io import StringIO

    session = Session(aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource("s3")

    filename_wo_ext = "image"
    filename_ext = "png"
    random_number = int(random.getrandbits(32))

    file_name = "image/{0}_{1}.{2}".format(filename_wo_ext,
                                           random_number, filename_ext)

    # Save image to JPEG
    image = cv2.imencode('.png', img)[1].tobytes()

    if sys.version_info[0] < 3:

        stream = StringIO.StringIO(image)
        stream.seek(0)
        image = stream.read()

    # Update Image to AWS
    s3.Bucket(aws_bucket_data).put_object(
        Key=file_name,
        Body=image,
        ACL="public-read"
    )

    image_url = "https://s3.amazonaws.com/{0}/{1}".format(
        aws_bucket_data, file_name)
    return image_url


def extract_roi(image, x, y, width, height):

    return image[y:y+height, x:x+width]


def b64_to_cv2(image):
    imgdata = base64.b64decode(image)
    buffer = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(buffer), cv2.COLOR_BGR2RGB)


def send_alert(message, check_name, slack_url,
               slack_username=SLACK_USERNAME, slack_channel=SLACK_CHANNEL):
    try:
        # Alert through Slack
        slack_dict = {"channel": slack_channel,
                      "username": slack_username,
                      "text": "{} alert".format(check_name),
                      "attachments": [{"fallback": "Alert",
                                       "text": message,
                                       "color": "#FF0000"}]}

        req = requests.post(slack_url,
                            json=slack_dict,
                            headers={'content-type': 'application/json'},
                            timeout=60)
        # Alert through Twilio
    except Exception as e:
        return {'error': 'slack post failed'}

def post_ubi_var(token, device="checks", variable="check-instance", value=1):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
        data = {variable: value}
        response_code = 400
        retries = 0

        while (response_code != 200 and retries <= 5):
            req = requests.post(url=url, headers=headers,
                            json=data)
            response_code = req.status_code
            if response_code == 200 or response_code == 201:
                return True
            retries += 1

        return False
    except Exception as e:
        print("[ERROR] {}".format(e))
        return False
