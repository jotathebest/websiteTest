
import os
from websiteTest.storage.storage import Storage


class LocalStorage(Storage):
    def __init__(self, *args, **kwargs):
        '''
        Inits the local Storage class
        @content_name: The name of the local file that will storage the content.
        @content_ext: File extension
        @content: String type. Content to be stored.
        '''
        self.storage_path = kwargs.get("content", None)
        self._base_dir = os.path.dirname(os.path.abspath(__file__))

    def save(self, content_name, content, content_ext="txt"):
        try:
            file_name = "{}.{}".format(content_name, content_ext)
            with open(os.path.join(self._base_dir, file_name), 'a') as f:
                f.write(content)
                f.write("\n")
            return True
        except Exception as e:
            print(e)
            return False

    def open(self, path_file):
        '''
        Returns a binary file from the path
        '''
        if not exist(path_file):
            message = "[ERROR] The file from path {}".format(path_file)
            message = "{} does not exist".format(message)
            raise LocalStorageError(message)

        string_read = ""
        with open(path_file, 'r') as f:
            string_read = f.read()

        return string_read

    def exist(self, path_file):
        '''
        Returns True if the file from the specified path exists
        '''
        return os.path.isfile(path_file)

class LocalStorageError(ValueError):
    pass
