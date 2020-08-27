import json
import os
import logging
import boto3
import time
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource("ec2")

def lambda_handler(event, context):

    logger.info(json.dumps(event))

    if event["operation"] == "START":
        print("STARTING")
        start_filters=[{'Name': 'tag:Scheduler', 'Values': ['24x7','Working']}]
        ec2.instances.filter(Filters=start_filters).start()

    elif event["operation"] == "STOP":
        print("STOPPING")    
        stop_filters=[{'Name': 'tag:Scheduler', 'Values': ['Turn off nightly','Working']}]
        ec2.instances.filter(Filters=stop_filters).stop()


    return
