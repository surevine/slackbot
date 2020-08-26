import json
import os
import logging
import urllib
import boto3
import time
import hashlib, hmac
import botocore.vendored.requests as requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))

    if not sent_from_surevine_slack(event):
        body = { "Response" : "Non-Authoritive access" }
        return {
            'statusCode' : 401,
            'body': json.dumps(body)
        }
    
    try:    
        send_slack_response(get_response_url(event))

        command = get_command(event)
        operation = command[0]
        target = command[1]
        
        invoke_lambda(operation, target)

    except Exception as e:
        logger.error(e)
        return { 'statusCode': 500 }

    return { 'statusCode': 200 }


def invoke_lambda(operation, target):
    lambda_client = boto3.client('lambda')

    inputParams = {
        "operation"   : operation,
        "target"      : target
    }
    lambda_client.invoke(
        FunctionName = os.environ["EC2_CONTROLLER_FUNCTION_ARN"],
        InvocationType='Event',
        Payload = json.dumps(inputParams)
    )    

def send_slack_response(response_url):

    response_body = { 
        "text": "*Thanks for your request, I am on it.*",
        "type": "mrkdwn"
    }

    headers = {
       'content-type': 'application/json'
    }

    try: 
        r = requests.post(response_url, data=json.dumps(response_body), headers=headers)
        status_code = r.status_code
        print(json.dumps(response_body))
        print(status_code)
        print(r.text)
    except Exception as e:
        print(e)


def sent_from_surevine_slack(event):

    if "body" not in event:
        raise Exception("Error, required information missing")
        
    slack_signature = event["headers"]["X-Slack-Signature"]
    slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"].encode('utf-8')
    timestamp = event["headers"]['X-Slack-Request-Timestamp']
    body = event['body'].encode('utf-8')
    
    five_minutes = 60 * 5
    if (time.time() - int(timestamp)) > five_minutes:
        return False
    
    timestamp = timestamp.encode('utf-8')
    base = 'v0:%s:%s' % (timestamp.decode('utf-8'), body.decode('utf-8'))
    
    computed = hmac.new(slack_signing_secret, base.encode('utf-8'),
                    digestmod=hashlib.sha256).hexdigest()
    computed_signature = 'v0=%s' % (computed,)

    return hmac.compare_digest(computed_signature, slack_signature)

def get_command(event):

    body = event["body"]
    qs = urllib.parse.parse_qs(body)
    
    if "text" not in qs:
        raise Exception("Error, required information missing")
    
    try:
        text = qs["text"]
        text = text[0]
        split_command = text.lower().split(' ', 1)
        print(split_command)
    except:
        raise Exception("Error, required information missing")
        
    if len(split_command) != 2:
        raise Exception("Error, requires two words")
        
    return split_command



def get_response_url(event):
        
    body = event["body"]
    qs = urllib.parse.parse_qs(body)
    
    if "response_url" not in qs:
        raise Exception("Error, response URL missing")

    return qs["response_url"][0]
