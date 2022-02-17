import os

import boto3


class S3:

    def __init__(self, bucket) -> None:
        self._bucket = bucket
        self.client = boto3.client('s3', region_name='ap-northeast-1')

    def upload(self, obj_key: str, obj_content: bytes = None, obj_path: str = '') -> None:
        if obj_content:
            self.client.put_object(ACL='private', Body=obj_content, Bucket=self._bucket, Key=obj_key)

        elif obj_path and os.path.isfile(obj_path):
            self.client.upload_file(obj_path, self._bucket, obj_key)
        else:
            raise Exception('Input Error')
