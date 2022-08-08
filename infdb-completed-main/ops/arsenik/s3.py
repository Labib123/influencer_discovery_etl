from datetime import datetime
import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
import logging

# boto3 S3 initialization
s3_client = boto3.client('s3')


CURRENT_DATE = datetime.today().strftime('%Y-%m-%d').replace("-", "")
raw_path = "./raw/instagram/"
raw_file = "{0}/ig_meta_{1}".format(raw_path, CURRENT_DATE)
bucket_name = "infdb-data-store-dev"


def add_to_raw_file(env, file, path, bucket_name):
    if env == "local":
        file_path = "~/s3_local/{0}/{1}".format(path, file)

        if not os.path.isfile(file_path):
            os.mknod(file_path)
    else:
        file_path = "/staging".format(path)
        try:
            response = s3_client.upload_file(file_path, bucket_name, file)

        except ClientError as e:
            logging.error(e)
            return False


