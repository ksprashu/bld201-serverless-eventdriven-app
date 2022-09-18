#!/usr/bin/env bash

# store-usernames function
echo "deploying average-scores api"
cd functions/api-average-scores/python > /dev/null
sh ./deploy.sh > deploy.log 2>&1 &
cd ../../.. > /dev/null

# store-scores function
echo "deploying round-attempts api"
cd functions/api-round-attempts/python > /dev/null
sh ./deploy.sh > deploy.log 2>&1 &
cd ../../.. > /dev/null

