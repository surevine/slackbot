import json
import os
import logging
import urllib
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONFLUENCE = "i-03c9b93a5e590d8df"
VPN = "i-010e9db190ec434d4"
GIT = "i-0241c0a8ea30ecf46"
DATABASE = "i-081ffee71f6238ad0"
AUTH_SERVICE = "i-0e690e2ee6448f38a"

groups = {
        "confluence": CONFLUENCE,
        "vpn": VPN,
        "git": GIT,
        "database": DATABASE,
        "auth service": AUTH_SERVICE
    }
    
region = "eu-west-2"
    
ec2 = boto3.client("ec2", region_name=region)
    
def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    
    try:    
        command = get_command(event)
        operation = command[0]
        target = command[1]
        response = perform_operation(operation, target)
    except Exception as e:
        body = { "Response" : str(e) }
        return {
            'statusCode': 200,
            "body" : json.dumps(body)
        }
    
    body = { "Response" : response }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def get_command(event):
    if "body" not in event:
        raise Exception("Error, required information missing")
        
    body = event["body"]
    qs = urllib.parse.parse_qs(body)
    
    if "text" not in qs:
        raise Exception("Error, required information missing")
    
    try:
        text = qs["text"]
        text = text[0]
        split_command = text.lower().split()
    except:
        raise Exception("Error, required information missing")
        
    if len(split_command) != 2:
        raise Exception("Error, requires two words")
        
    return split_command

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
        ec2.start_instances(InstanceIds = [groups[target]])
        return "Starting " + target + "..."
    except:
        raise Exception("Service not found")
    
def stop(target):
    try:
        ec2.stop_instances(InstanceIds = [groups[target]])
        return "Stopping " + target + "..."
    except:
        raise Exception("Service not found")
