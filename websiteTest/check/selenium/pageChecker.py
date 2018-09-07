from .baseChecker import SeleniumBaseChecker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import tools

import base64


class PageChecker(SeleniumBaseChecker):
    def __init__(self, storage, *args, **kwargs):
        '''
        @storage must be an instance from the storage module to
        read or save files from AWS or local files
        '''
        super().__init__(*args, **kwargs)
        self.storage = storage

    def load_url(self, url, webelement_to_wait, timeout):
        print("[INFO] Loading website")
        self.browser.set_page_load_timeout(timeout)
        self.browser.get(url)
        element_exists = True

        if webelement_to_wait is not None:
            element_exists = search_webelement(webelement_to_wait, timeout)

        print("[INFO] Finished")

        if not element_exists:
            message = "[ERROR] The webelement {}".format(webelement_to_wait)
            message = "{} is not present in the webpage".format(message)
            raise PageCheckerError(message)

    def search_webelement(self, webelement_to_wait, timeout):
        try:
            # Waits until web_element to wait is loaded
            element = WebDriverWait(self.browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                self.webelement_to_wait
                                                ))
            )
            return True

        except Exception as e:
            message = "[ERROR] Could not load website properly,"
            message = "{} details below \n {}".format(message, e)
            print(message)
            return False

    def open_template(self, path):
        img_bytes = self.storage.open(path)
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        self.template = tools.b64_to_cv2(b64)

    def tester(self, url, template_path, delta=0.5,
               webelement_to_wait=None, timeout=60):
        '''
        Returns True if images are different
        @url: Website URL to test
        @template_path: path to the template
        @delta: Max difference delta between the images
        @web_element_to_wait: Optional. Web element to search in the website
        @timeout: Max timeout for page load
        '''
        self.open_template(template_path)
        self.load_url(url, webelement_to_wait, timeout)

        b64 = self.browser.get_screenshot_as_base64()
        testing = tools.b64_to_cv2(b64)

        result = tools.compare_images(self.template, testing, delta=delta)
        return (result, self.template, testing)

    def create_template(self, url, template_name, template_ext='png',
                        webelement_to_wait=None, timeout=60):
        '''
        stores a template of the website
        '''

        self.load_url(url, webelement_to_wait, timeout)
        b64 = self.browser.get_screenshot_as_base64()
        template = tools.b64_to_bytes(b64)
        result = self.storage.save(binary_file=template,
                                   file_ext=template_ext,
                                   file_name=template_name)
        return result

    def close_browser(self):
        self.browser.quit()


class PageCheckerError(ValueError):
    """docstring for SeleniumError"""


pass
