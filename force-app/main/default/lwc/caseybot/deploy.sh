#!/bin/bash

# Authenticate with Salesforce
sfdx auth:jwt:grant --clientid $CONSUMER_KEY --jwtkeyfile <(echo "$SF_JWT_KEY") --username $USERNAME --instanceurl https://login.salesforce.com --setdefaultdevhubusername

# Deploy the source to Salesforce
sfdx force:source:deploy -p force-app -u $USERNAME
