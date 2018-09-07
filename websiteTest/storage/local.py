from storage.storage import Storage
import os

class LocalStorage(Storage):
    def __init__(self, *args, **kwargs):
        '''
        Inits the local Storage class
        @file_name: The name of the local file that will storage the binary_file.
        @file_ext: File extension
        @binary_file: String type. binary_file to be stored.
        '''

    def save(self, file_name, binary_file, file_ext="txt"):
        try:
            file_name = "{}.{}".format(file_name, file_ext)
            with open(file_name, 'w+b') as f:
                f.write(binary_file)
            return True
        except Exception as e:
            print(e)
            return False

    def open(self, path_file):
        '''
        Returns a binary file from the path
        '''
        if not self.exist(path_file):
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
