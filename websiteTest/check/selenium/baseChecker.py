from selenium import webdriver
from utils import tools
import cv2


class BaseChecker(object):
    """BaseChecker should be inherited in all the checkers subclasses"""

    def __init__(self, aws_secret_access_key, aws_access_key_id,
                 aws_bucket_data, slack_url, path_testing="testing",
                 path_template="templates",  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.aws_bucket_data = aws_bucket_data
        self.path_testing = path_testing
        self.path_template = path_template
        self.slack_url = slack_url

    def compare(self, testing_name, template_name):
        '''
        Reads images from DD and compares them
        '''
        testing_path = "{}/{}.png".format(self.path_testing, testing_name)
        self.image_testing = cv2.imread(testing_path)

        template_path = "{}/{}.png".format(self.path_template, template_name)
        self.image_template = cv2.imread(template_path)

        return (tools.compare_images(self.image_template, self.image_testing))

    def paint_image_difference(self):
        '''
        Return a numpy array with the mask of differences
        '''
        result = cv2.absdiff(self.image_testing, self.image_template)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        if cv2.countNonZero(gray) <= 0:
            return result

        ret, thresh = cv2.threshold(gray, 1, 255, 0)
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]
        cv2.drawContours(result, cnts, -1, (0, 0, 255), 1)
        return result

    def upload_s3(self, image):
        image_url = tools.send_to_s3(image, self.aws_access_key_id,
                                     self.aws_secret_access_key,
                                     self.aws_bucket_data)
        return image_url

    def send_alert(self, templates, testings, differences):

        if len(testings) > 0:
            message = "[ALERT] Sending alert through Slack with"
            message = "{} wrong images".format(message)
            print(message)

            for key in testings.keys():
                alert_message = ""
                alert_message = "{0}*{1}*\n-Template image url: {2}\n".format(
                    alert_message,
                    key.capitalize(),
                    templates[key])
                alert_message = "{0}-Tested image url: {1}\n".format(
                    alert_message,
                    testings[key])
                alert_message = "{0}-Differences mask url: {1}\n".format(
                    alert_message,
                    differences[key])
                tools.send_alert(alert_message, key, self.slack_url)
            return False

    def tester(self):
        raise NotImplementedError(
            "Please implement a tester() method in your class")

    def create_template(self):
        raise NotImplementedError(
            "Please implement a create_templates() method in your class")
