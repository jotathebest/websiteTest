from ..base.check import BaseChecker
from utils import tools

import requests


class ApiPost(BaseChecker):
    def __init__(self, storage, *args, **kwargs):
        '''
        @storage must be an instance from the storage module to
        read or save files from AWS or local files
        '''
        super().__init__(*args, **kwargs)
        self.storage = storage

    def make_post(self, url, headers, data, timeout):
        '''
        Makes a POST request to a website and returns the server answer in bytes
        @url: Url to make the POST request
        @headers: POST request headers
        @data: Data to send
        '''
        try:
            req = requests.post(url=url, headers=headers,
                                data=data, timeout=timeout)
            status_code = req.status_code

            return req.text
        except Exception as e:
            raise ApiPostError("[ERROR] Error posting, details: {}".format(e))

    def open_template(self, path):
        self.template = self.storage.open(path)

    def tester(self, url, headers, data, template_path, timeout=60):
        '''
        Returns True if images are different
        @url: Website URL to test
        @template_path: path to the template
        @timeout: Max timeout for page load
        '''
        self.open_template(template_path)
        testing = self.make_post(url, headers, data, timeout=timeout)

        result = (self.template == testing)
        return (result, self.template, testing)

    def create_template(self, url, headers, data, template_name,
                        template_ext='txt', timeout=60):
        '''
        stores a template of the POST request result website
        '''

        template = self.make_post(url, headers, data, timeout)

        result = self.storage.save(binary_file=template.encode(),
                                   file_ext=template_ext,
                                   file_name=template_name)
        return result


class ApiPostError(ValueError):
    """docstring for SeleniumError"""
    pass
