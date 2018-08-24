
class Storage(object):


    def save(self, *args, **kwargs):
        raise NotImplementedError(
            "Please implement a save() method in your class")

    def open(self, *args, **kwargs):
        raise NotImplementedError(
            "Please implement a open() method in your class")

    def exist(self, *args, **kwargs):
        raise NotImplementedError(
            "Please implement a exist() method in your class")
