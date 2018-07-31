
class BaseChecker(object):
    """BaseChecker should be inherited in all the checkers subclasses"""

    def __init__(self, storage=None):
        self.storage = storage
 
    def tester(self):
        raise NotImplementedError(
            "Please implement a tester() method in your class")

    def create_template(self):
        raise NotImplementedError(
            "Please implement a create_templates() method in your class")
