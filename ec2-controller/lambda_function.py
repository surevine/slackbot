import json
import os
import logging
import urllib
import boto3
import time
import hashlib, hmac
logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = "eu-west-2"
    
ec2 = boto3.client("ec2", region_name=region)
    
def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    
   
