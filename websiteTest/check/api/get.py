from ..base.check import BaseChecker
from utils import tools

import requests


class ApiGet(BaseChecker):
    def __init__(self, storage, *args, **kwargs):
        '''
        @storage must be an instance from the storage module to
        read or save files from AWS or local files
        '''
        super().__init__(*args, **kwargs)
        self.storage = storage

    def make_get(self, url, headers, timeout):
        '''
        Makes a POST request to a website and returns the server answer in bytes
        @url: Url to make the POST request
        @timeout: Max time to wait for server response
        '''
        try:
            req = requests.get(url=url, headers=headers, timeout=timeout)
            status_code = req.status_code

            return req.text
        except Exception as e:
            raise ApiGetError("[ERROR] Error getting, details: {}".format(e))

    def open_template(self, path):
        self.template = self.storage.open(path).decode("utf-8")

    def tester(self, url, headers, template_path, timeout=60):
        '''
        Returns True if testing and template are different
        @url: Website URL to test
        @headers: Headers for the request
        @template_path: path to the template
        @timeout: Max timeout for page load
        '''
        self.open_template(template_path)
        testing = self.make_get(url, headers, timeout)

        result = not (testing == self.template)
        return (result, self.template, testing)

    def create_template(self, url, headers, template_name,
                        template_ext='txt', timeout=60):
        '''
        stores a template of the POST request result website
        '''

        template = self.make_get(url, headers, timeout)

        result = self.storage.save(binary_file=template.encode(),
                                   file_ext=template_ext,
                                   file_name=template_name)
        return result


class ApiGetError(ValueError):
    """docstring for SeleniumError"""
    pass
