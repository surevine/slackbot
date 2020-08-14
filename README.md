# slackbot

This code is pushed to a Lambda in AWS by the GitHub Action.

## Connect to Slack
To connect the Lambda to Slack:

Create an API gateway with ANY method being sent to the Lambda. (should only  _need_ POST)

Create an app in Slack (https://api.slack.com/apps)

Under **Features** :

Grant the app : app_mentions:read channels:join chat:write chat:write.customize incoming-webhook commands

(These may not all be needed now)

Create a new slash command "surevinebot" with a target URL of your API gateway endpoint.

Under **Settings: Basic information** : Add the app to the workspace.

## First steps
In your Lamdba, return the request as json and slack will display it. You can also log the full request to Cloudwatch.

This should help you understand where to go next!

eg.

	import json
	import os
	import logging
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	def lambda_handler(event, context):
	    logger.info('## ENVIRONMENT VARIABLES')
	    logger.info(os.environ)
	    logger.info('## EVENT')
	    logger.info(event)
	    body = {"Request " : event["body"] }
	    return {
	        'statusCode': 200,
	        'body': json.dumps(body)
	    }
