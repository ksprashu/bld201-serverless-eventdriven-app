#!/usr/bin/env bash

# store-usernames function
echo "deploying store-usernames function"
cd functions/store-usernames/python > /dev/null
sh ./deploy.sh > deploy.log 2>&1 &
cd ../../.. > /dev/null

# store-scores function
echo "deploying store-scores function"
cd functions/store-scores/python > /dev/null
sh ./deploy.sh > deploy.log 2>&1 &
cd ../../.. > /dev/null

