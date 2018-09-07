from ..base.check import BaseChecker
from selenium import webdriver

class SeleniumBaseChecker():
    """BaseChecker should be inherited in all the checkers subclasses"""

    def __init__(self, *args, **kwargs):
        width = kwargs.get("width", 1386)
        height = kwargs.get("height", 768)
        self.create_browser(width, height)
        self.timeout = kwargs.get("timeout", 30)
        self.browser.set_page_load_timeout(self.timeout)  # Max timeout to load a page


    def create_browser(self, width, height):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False
        })
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_window_size(width, height)

    def tester(self):
        raise NotImplementedError(
            "Please implement a tester() method in your class")

    def create_template(self):
        raise NotImplementedError(
            "Please implement a create_templates() method in your class")
