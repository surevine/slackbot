import json
import os
import logging
import urllib
import boto3
import time
import hashlib, hmac

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    
    return { 'statusCode': 200 }
