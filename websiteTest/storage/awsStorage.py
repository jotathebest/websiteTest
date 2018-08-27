import random
import requests

from boto3.session import Session
from websiteTest.storage.storage import Storage


class AwsStorage(Storage):
    """
    AWS S3 storage instance. Requires AWS keys to put remote objects.
    For more information about how to retrieve these keys, refer 
    to the official AWS docs.
    """

    def __init__(self, aws_secret_access_key, aws_access_key_id, aws_bucket):
        """
        @aws_secret_access_key: Amazon secret key
        @aws_access_key_id: Amazon Access key
        @aws_bucket: Amazon remote buckte to store files
        """
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.aws_bucket = aws_bucket

    def init_session(self):

        session = Session(aws_access_key_id=self.aws_access_key_id,
                          aws_secret_access_key=self.aws_secret_access_key)
        s3 = session.resource("s3")

        return s3

    def save(self, binary_file, file_ext, file_name=None,
             access_policy="public-read"):
        """
        Sends a binary file to AWS
        @binary_file: File to send must be a binary file type.
        @file_ext: File extension txt, ino, png, etc
        @file_name: Optional, if not set, a random number will be used
        @access_policy: Policy access of the file,'public-read' by default
        """

        s3 = self.init_session()

        if file_name is None:
            file_name = random_number = int(random.getrandbits(32))

        file_name = "{0}.{1}".format(file_name, file_ext)

        # Sends file to AWS
        s3.Bucket(self.aws_bucket).put_object(
            Key=file_name,
            Body=binary_file,
            ACL=access_policy
        )

        file_url = "https://s3.amazonaws.com/{0}/{1}".format(
            self.aws_bucket, file_name)
        return file_url

    def open(self, file_url, timeout=60):
        """
        Returns a binary file from the url
        """
        re = requests.get(file_url, timeout=timeout)

        if re.status_code >= 400:  # The file does not exist
            return None

        return re.content

    def exist(self, file_name=None, aws_bucket=None):
        """
        Returns True if the AWS file exist in the specified remote path
        """
        if aws_bucket is None:
            aws_bucket = self.aws_bucket

        s3 = self.init_session()
        bucket = s3.Bucket(aws_bucket)
        objs = list(bucket.objects.filter(Prefix=file_name))
        if len(objs) > 0 and objs[0].key == file_name:
            return True
        else:
            return False
