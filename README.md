# slackbot

This code is pushed to a Lambda in AWS by the GitHub Action.

Create an API gateway with ANY method being sent to the Lambda.

Create an app in Slack (https://api.slack.com/apps)

Under features :

Grant the app : app_mentions:read  channels:join chat:write chat:write.customize incoming-webhook commands

Create a new slash command "surevinebot" with a target URL of your API gateway endpoint.
Under Settings: Basic information :
Add the app to the workspace.

In your lamdba, initially return the request as json and slack will display it. This should help you understand where to go.
