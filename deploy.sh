#!/bin/bash

# Authenticate with Salesforce
sfdx auth:jwt:grant --clientid $CONSUMER_KEY --jwtkeyfile <(echo "$SF_JWT_KEY") --username $SALESFORCE_USERNAME --instanceurl https://login.salesforce.com --setdefaultdevhubusername

# Check if authentication was successful
if [ $? -ne 0 ]; then
    echo "Error: Authentication with Salesforce failed"
    exit 1
fi

# Deploy the source to Salesforce
sfdx force:source:deploy -p force-app -u $SALESFORCE_USERNAME

# Check if deployment was successful
if [ $? -ne 0 ]; then
    echo "Error: Deployment to Salesforce failed"
    exit 1
fi

echo "Deployment to Salesforce succeeded"
