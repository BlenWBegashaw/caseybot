#!/bin/bash

# Authenticate with Salesforce
sfdx auth:jwt:grant --clientid $SF_CLIENT_ID --jwtkeyfile server.key --username $SF_USERNAME --instanceurl https://login.salesforce.com --setdefaultdevhubusername

# Deploy the source to Salesforce
sfdx force:source:deploy -p force-app -u $SF_USERNAME
