import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    x = event["body"].find('user_name')
    y = event["body"].find("&", x + 10, x + 35)
    text = event["body"]
    user_name = text[x + 10 : y]
    body = {"Hello " : user_name }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
