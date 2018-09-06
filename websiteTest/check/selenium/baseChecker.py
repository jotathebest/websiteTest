from selenium import webdriver

class BaseChecker():
    """BaseChecker should be inherited in all the checkers subclasses"""

    def __init__(self, *args, **kwargs):
        self.browser = webdriver.Chrome()
        self.timeout = kwargs.get("timeout", 30)
        self.browser.set_timeout(self.timeout)  # Max timeout to load a page

    def tester(self):
        raise NotImplementedError(
            "Please implement a tester() method in your class")

    def create_template(self):
        raise NotImplementedError(
            "Please implement a create_templates() method in your class")
