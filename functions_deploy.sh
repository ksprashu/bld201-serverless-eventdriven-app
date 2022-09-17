#!/usr/bin/env bash

# store-usernames function
echo "deploying store-usernames function"
gcloud functions deploy store-usernames \
--gen2 \
--trigger-http \
--runtime=python310 \
--region=us-west1 \
--source=functions/store-usernames/python/. \
--entry-point="event_receiver"

# store-scores function
echo "deploying store-usernames function"
gcloud functions deploy store-scores \
--gen2 \
--trigger-http \
--runtime=python310 \
--region=us-west1 \
--source=functions/store-scores/python/. \
--entry-point="event_receiver"
