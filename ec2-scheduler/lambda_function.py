import json
import os
import logging
import boto3
import time
import botocore.vendored.requests as requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource("ec2")

def lambda_handler(event, context):

    logger.info(json.dumps(event))

    if event["operation"] == "START":
        print("STARTING")
        send_slack_message("Starting instances")
        start_filters=[{'Name': 'tag:Scheduler', 'Values': ['24x7','Working']}]
        ec2.instances.filter(Filters=start_filters).start()

    elif event["operation"] == "STOP":
        print("STOPPING")
        send_slack_message("Stopping instances")
        stop_filters=[{'Name': 'tag:Scheduler', 'Values': ['Turn off nightly','Working']}]
        ec2.instances.filter(Filters=stop_filters).stop()

    return

def send_slack_message(message_text):
    
    message_body = { 
        "channel": os.environ["SLACK_GENERAL_CHANNEL_ID"],
        "text": message_text,
        "type": "mrkdwn"
    }

    headers = {
       'content-type': 'application/json',
       'Authorization': 'Bearer ' + os.environ["SLACK_OAUTH_TOKEN"]
    }

    try: 
        r = requests.post(os.environ["SLACK_POST_MESSAGE_ENDPOINT"], data=json.dumps(message_body), headers=headers)
        status_code = r.status_code
        print(json.dumps(message_body))
        print(status_code)
        print(r.text)
    except Exception as e:
        print(e)
