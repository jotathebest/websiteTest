import checkers as chks
import settings
import numpy as np
import os

from selenium import webdriver
from pyvirtualdisplay import Display
from utils import tools


class Tester():

    def __init__(self, checkers, checker_prefix='check'):
        self.initialization(checkers, checker_prefix)
        self.check_prefix = checker_prefix
        self.widgets = {}
        self.widget_presence = False

    def initialization(self, checkers, checker_prefix):
        self.all_checkers = [c[len(checker_prefix) + 1:]
                             for c in settings.config.sections()
                             if c.startswith(checker_prefix)]
        if len(self.all_checkers) <= 0:
            raise ExceptionTester(
                "could not find any checker with the specified id")

        if "all" in checkers:
            self.checkers = self.all_checkers

        else:
            chk = set()
            for check in checkers:
                choosed = {j for j in self.all_checkers if j.startswith(
                    check + ":") or j == check}
                chk.update(choosed)
            self.checkers = list(chk)

    def create_tester(self, checker, browser):
        tester_type, name = checker.split(":")
        kwargs = dict(settings.config["general"])
        section = "{}_{}".format(self.check_prefix, checker)
        kwargs.update(dict(settings.config[section]))
        kwargs.update({"browser": browser})
        kwargs.update({"widgets": self.widgets})
        kwargs.update({"widget_presence": self.widget_presence})
        kwargs.update({"widget_name": name})
        tester_instance = getattr(
            chks, "{}Tester".format(tester_type.capitalize()))
        return tester_instance(**kwargs)

    def create_templates(self):
        print("[INFO] creating browser and tester instances")
        display = Display(visible=0, size=(1386, 768))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False
        })
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.set_window_size(1386, 768)

        for checker in self.checkers:
            tester_instance = self.create_tester(checker, browser)
            tester_instance.create_template()

        browser.quit()

    def tester(self):
        templates = {}
        testings = {}
        differences = {}
        print("[INFO] creating browser and tester instances")
        display = Display(visible=0, size=(1386, 768))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False
        })
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.set_window_size(1386, 768)

        for checker in self.checkers:
            tester_type, name = checker.split(":")
            tester_instance = self.create_tester(checker, browser)
            print("[INFO] running tester for checker: {}".format(checker))

            (test_result, template, testing) = tester_instance.tester()
            if test_result or test_result is None:
                print("[ALERT] images from test for")
                print(" {} do not fit".format(checker))
                templates[name] = tester_instance.upload_s3(template)
                testings[name] = tester_instance.upload_s3(testing)
                try:
                    difference_url = tester_instance.upload_s3(
                        tester_instance.paint_image_difference())
                except Exception as e:
                    # If there is any error, uploads a black image and alerts
                    mask = np.ones((320, 240))
                    mask_url = tester_instance.upload_s3(mask)
                    difference_url = mask_url

                differences[name] = difference_url

            print("[INFO] finished tester for checker {}".format(checker))

        browser.quit()
        if len(differences) > 0:
            print("[ALERT] sending alert")
            tester_instance.send_alert(templates, testings, differences)

        print("[INFO] Confirming to Ubidots the end of the routine")
        tools.post_ubi_var(dict(settings.config['general'])['token'])
        print("[INFO] Finished")


class ExcepectionTester(Exception):
    def __init__(self, msg):
        self.msg = msg
        print(self.msg)
