"""
@title: s3_aws_automation
@description: create s3 bucket and apply policies.
"""
import argparse
import json
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
        host = os.getenv("MINIO_HOST")
        self.log.debug(f"[+] connecting to {host}")
        minioClient = Minio(
            host,
            access_key=os.getenv("ACCESS_KEY"),
            secret_key=os.getenv("SECRET_KEY"),
            secure=False
        )
        return minioClient

    def loadPolicy(self, policyJson):
        self.log.info(f"[+] loading {policyJson}")
        policyJsonDir = os.path.dirname(__file__)
        policyJsonFile = os.path.join(policyJsonDir, policyJson)
        if os.path.exists(policyJsonFile):
            self.log.debug(f"[+] {policyJsonFile} is exists.")
            with open(policyJsonFile) as jsonFile:
                policy = json.load(jsonFile)
                return policy
        else:
            self.log.error("[-] policy file not found, please check file path and try again!!")

    def s3BucketCreation(self, s3BucketName, policyfiles):
        minioClient = self.initMinio()
        try:
            self.log.info("[+] creating S3 bucket . . .")
            minioClient.make_bucket(s3BucketName, location=os.getenv("AWS_REGION "))
            self.log.debug("[+] successfully created bucket.")
            self.log.info(f"checking created S3 bucket . . .")
            buckets = minioClient.list_buckets()
            for bucket in buckets:
                if bucket.name == s3BucketName:
                    self.log.debug(f"[+] S3 bucket is exists "
                                   f"bucket name :{bucket.name} created at {bucket.creation_date}")

                    for pFile in policyfiles:
                        self.log.debug(f"[+] reading policies from {pFile}")
                        policy = self.loadPolicy(pFile)
                        self.log.info("[+] applying access policies on S3 bucket")
                        minioClient.set_bucket_policy(s3BucketName, json.dumps(policy))
                        self.log.debug("[+] policy updated on bucket")
                        self.log.debug(f"[+] get bucket policy \n"
                                       f"{minioClient.get_bucket_policy(s3BucketName)}")
        except S3Error as exc:
            self.log.error(f"[-] exception caused at\n"
                           f"{exc}")


s3Object = S3_Automation()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3bucket", type=str, required=True, help="please enter s3 bucket name")
    parser.add_argument("--policyfiles", nargs="+", required=True,
                        help="Please list the policy files ex.(file1 file2 ...)")
    args = parser.parse_args()
    s3Object.s3BucketCreation(args.s3bucket, args.policyfiles)
    pass
