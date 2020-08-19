import json
import os
import logging
import urllib
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    region = "eu-west-2"
    instances = {
        "confluence": "i-03c9b93a5e590d8df",
        "vpn": "i-010e9db190ec434d4",
        "git": "i-0241c0a8ea30ecf46",
        "database": "i-081ffee71f6238ad0",
        "auth service": "i-0e690e2ee6448f38a"
    }
    ec2 = boto3.client("ec2", region_name=region)
    
    if "body" not in event:
        return {
            'statusCode': 500,
            "Response" : "Error, required information missing"
        }
        
    body = event["body"]
    qs = urllib.parse.parse_qs(body)
    
    if "text" not in qs:
        return {
            'statusCode': 400,
            "Response" : "Error, required information missing"
        }
    try:
        text = qs["text"]
        text = text[0]
        split_command = text.lower().split()
        operation = split_command[0]
        target = split_command[1]
    except:
        return {
            "statusCode" : 400,
            "Response" : "Error, required information missing"
        }
    def start(target):
        try:
            ec2.start_instances(InstanceIds = [instances[target]])
            return "Starting " + target + "..."
        except:
            return {
                'statusCode': 404,
                'Response': "Service not found"
            }

    def stop(target):
        try:
            ec2.stop_instances(InstanceIds = [instances[target]])
            return "Stopping " + target + "..."
        except:
            return {
                'statusCode': 404,
                'Response': "Service not found"
            }
            
    if operation == "start":
        response = start(target)
    elif operation == "stop":
        response = stop(target)
    else:
        return {
        'statusCode': 404,
        'Response': "Command not recognised"
    }
    
    body = { "Response" : response }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
