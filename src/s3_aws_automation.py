"""
@title: s3_aws_automation
@description: create s3 bucket and apply policies.
"""
import argparse
import logging
from colorlog import ColoredFormatter
from minio import Minio
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)


class S3_Automation(object):
    def logger(self):
        log = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        formatter = ColoredFormatter(
            '%(log_color)s %(process)d-%(levelname)s-%(message)s', '%c')
        ch.setFormatter(formatter)
        log.addHandler(ch)
        log.setLevel(logging.DEBUG)
        log.propagate = False
        return log

    def initMinio(self):
        # initialize miniClient with an endpoint and access/secret keys.
        log = self.logger()
        log.info("[+] INITIALIZE THE MINIO CLIENT")
        minioClient = Minio(
            'play.min.io:9000',
            access_key='Q3AM3UQ867SPQQA43P2F',
            secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
            secure=True
        )

        pass


s3Object = S3_Automation()
if __name__ == '__main__':
    s3Object.initMinio()
    pass
