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

## Update:
Slackbot authenticates requests to verify that they derive from our slack (using standard slack auth methods), relay requests after 5 minutes are denied access, preventing a relay attack.

Text from request is checked for valid command (currently "start", "stop", and a service name) and a valid command is not present, a fitting error message/ user info is returned.

Instances are turned on/off through EC2 with the python library boto3. If an instance needs another to be on for it to work, then that instance (given it's stated in the tags under "dependants") will also be turned on.

A cloudwatch scheduler event triggers the turning on/off of instances with the "working" tag and sends a message to the general chat regularly at 8 (am/pm).

## Future improvements:
Feature allowing users to delay instance shutdown and/or warn of an impending shutdown, via a slack message. FYI this may require a "que" between scheduler and ec2_scheduler lambda.

A feature that would mean if someone else is using a service that depends on another (the VPN for example) then it won’t shut down if another person tells it to as it is still in use.
