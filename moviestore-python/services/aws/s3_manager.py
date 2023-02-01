import json
import logging

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class S3Manager:
    """
    Class to handle all interactions with S3
    """

    def __init__(self, aws_region):
        self.aws_region = aws_region
        self.aws_session = boto3.Session(region_name=aws_region)
        self.client = self.aws_session.client('s3')

    def get_file_content(self, bucket_name, file_path):
        """
        Get the file content from S3
        :param bucket_name:
        :param file_path:
        :return:
        """
        response = self.client.get_object(Bucket=bucket_name, Key=file_path)
        file_content = response.get('Body').read().decode('utf-8')
        if file_content:
            file_data = json.loads(file_content)
        else:
            logger.error(f"Unable to find the path {file_path} inside bucket {bucket_name}")
            raise ValueError('No such s3 object')

        return file_data
