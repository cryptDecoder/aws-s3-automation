"""
@title: s3_aws_automation
@description: create s3 bucket and apply policies.
"""
import argparse
import logging
from colorlog import ColoredFormatter
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from pathlib import Path
import os


class S3_Automation(object):
    load_dotenv()

    log = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    formatter = ColoredFormatter(
        '%(log_color)s %(process)d-%(levelname)s-%(message)s', '%c')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    def initMinio(self):
        # initialize miniClient with an endpoint and access/secret keys.
        self.log.info("[+] INITIALIZE THE MINIO CLIENT")
        minioClient = Minio(
            'play.min.io:9000',
            access_key=os.getenv("ACCESS_KEY"),
            secret_key=os.getenv("SECRET_KEY"),
            secure=True
        )
        return minioClient

    def s3BucketCreation(self, s3BucketName):
        minioClient = self.initMinio()
        try:
            self.log.info("[+] creating S3 bucket . . .")
            minioClient.make_bucket(s3BucketName, location=os.getenv("AWS_REGION "))
            self.log.debug("[+] successfully created bucket.")

        except S3Error as exc:
            self.log.error(f"[-] exception caused at\n"
                           f"{exc}")


s3Object = S3_Automation()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3bucket", type=str, required=True, help="please enter s3 bucket name")
    args = parser.parse_args()
    s3Object.s3BucketCreation(args.s3bucket)
    pass
