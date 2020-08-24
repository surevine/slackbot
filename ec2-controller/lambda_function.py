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

CONFLUENCE = "i-03c9b93a5e590d8df"
VPN = "i-010e9db190ec434d4"
GIT = "i-0241c0a8ea30ecf46"
DATABASE = "i-081ffee71f6238ad0"
AUTH_SERVICE = "i-0e690e2ee6448f38a"

groups = {
        "confluence": [DATABASE, AUTH_SERVICE, VPN, CONFLUENCE],
        "vpn": [VPN],
        "git": [VPN, DATABASE, GIT]
    }

    
def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    
    try:    
        response = perform_operation("start", "git")
    except Exception as e:
        body = { "Response" : str(e) }
        return {
            'statusCode': 200,
            "body" : json.dumps(body)
        }
    
    return {
        "response": response
    }
    
def perform_operation(operation, target):
    if operation == "start":
        response = start(target)
    elif operation == "stop":
        response = stop(target)
    else:
        raise Exception("Command not recognised")
    return response
    
def start(target):
    try:
        ec2.start_instances(InstanceIds = groups[target])
        return "Starting " + target + "..."
    except Exception as e:
        logger.error(e)
        raise Exception("failed to start")
        
    
def stop(target):
    try:
        ec2.stop_instances(InstanceIds = groups[target])
        return "Stopping " + target + "..."
    except:
        raise Exception("Service not found")
   
