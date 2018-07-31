from .baseChecker import BaseChecker
from .signCheck import SignCheck
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.dashboard import Dashboard
from utils import tools
import time
import cv2

TIMEOUT = 30

# Coordinates [y, height, x, width]
special_pages = {"app_devices": [[275, 290, 50, 130]],
                 "page_devices": [[275, 290, 50, 130], [275, 290, 380, 460]]
                 }


class PageTester(BaseChecker, SignCheck):
    """docstring for WidgetTester"""

    def __init__(self, account_username, account_password, login_username,
                 login_password, token, make_login, webelement_to_wait,
                 page_name, sign_url, use_account_username, signout_url,
                 browser=None, page_url=None, check_all=True, *args, **kwargs):
        self.browser = browser if browser is not None else webdriver.Firefox()
        # Flag to know if the browser instance should be close
        # after reading the widgets
        self._browser = False if browser is not None else True
        kwargs["url"] = sign_url
        kwargs["signout_url"] = signout_url

        if use_account_username == "True":
            kwargs["username"] = account_username
            kwargs["password"] = account_password
        else:
            kwargs["username"] = login_username
            kwargs["password"] = login_password
        super(PageTester, self).__init__(*args, **kwargs)

        self.token = token
        self.page_url = page_url
        self.make_login = make_login
        self.webelement_to_wait = webelement_to_wait
        self.page_name = page_name
        self.check_all = check_all

    def adapt_page(self, image, image_name):
        '''
        This function is intended to patch with zeros places that
        can change in the long time (like the last update date of the
        device)
        '''
        coordinates = special_pages.get(image_name, None)
        if coordinates is None:
            return image

        for coordinate in coordinates:
            y, h, x, w = coordinate
            image[y:h, x:w] = [255, 255, 255]

        return image

    def load_url(self):
        if self.make_login == 'True':
            # makes signout if was previously logged
            if self.browser.current_url != self.url:
                self.sign_out()
            print("[INFO] Attempting to make login")
            sign_result = self.sign_in()

            if not sign_result:
                print("[ERROR] could not make login")
                return False

        # Waits until web_element to wait is loaded
        self.browser.get(self.page_url)

        try:
            print("[INFO] Loading website")
            element = WebDriverWait(self.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                self.webelement_to_wait
                                                ))
            )
            time.sleep(3)  # Gives additional 3 seconds to load the page
            return True

        except Exception as e:
            message = "[ERROR] Could not load website properly,"
            message = "{} details below \n {}".format(message, e)
            print(message)
            return False

    def get_screenshot(self):
        b64 = self.browser.get_screenshot_as_base64()
        return tools.b64_to_cv2(b64)

    def tester(self, testing_file_name="testing"):
        if not self.load_url():
            # Could not load properly the website
            b64 = self.browser.get_screenshot_as_base64()
            testing = tools.b64_to_cv2(b64)
            template_path = "{}/{}.png".format(self.path_template, self.page_name)
            template = cv2.imread(template_path)
            self.sign_out()
            return (True, template, testing)

        testing_path = "{}/{}.png".format(self.path_testing, testing_file_name)

        b64 = self.browser.get_screenshot_as_base64()
        testing = tools.b64_to_cv2(b64)

        if self.page_name in special_pages:
            testing = self.adapt_page(testing, self.page_name)

        template_path = "{}/{}.png".format(self.path_template, self.page_name)
        template = cv2.imread(template_path)
        print("[INFO] Testing page {}".format(self.page_name))

        self.image_testing = testing
        self.image_template = template

        if self.make_login == 'True':
            self.sign_out()

        if self._browser:  # If browser is an instance of the class, closes it
            self.browser.quit()

        print("[INFO] finished")
        return (tools.compare_images(template, testing, delta=0.5),
                template,
                testing)

    def create_template(self, widgets=None):
        ''' stores widgets templates locally '''
        print("[INFO] Making test for page {}".format(self.page_name))

        if not self.load_url():
            # Could not load properly the website
            self.sign_out()
            return False

        template_path = "{}/{}.png".format(self.path_template,
                                           self.page_name)

        print("[INFO] Saving template from page {}".format(self.page_name))
        result = self.browser.save_screenshot(template_path)

        if self.page_name in special_pages:
            image = cv2.imread(template_path)
            image = self.adapt_page(image, self.page_name)
            cv2.imwrite(template_path, image)

        if self.make_login == 'True':
            self.sign_out()

        if self._browser:  # If browser is an instance of the class, closes it
            self.browser.quit()

        print("[INFO] finished")
        return result
