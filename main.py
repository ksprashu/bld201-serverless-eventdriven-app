#!/usr/bin/env python

# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ast import Raise
import functions_framework
import json
import re

from google.cloud import storage
from google.cloud import firestore


@functions_framework.cloud_event
def event_receiver(cloud_event):
    """
    Event receiver called when an object is uploaded in the bucket

    Parameters:
        cloud_event (Object): Object passed into the event handler
    """

    print(f"Received event with ID: {cloud_event['id']}")
    data = cloud_event.data
    filename = data["name"]
    bucket_name = data["bucket"]
    store_scores(bucket_name, filename)


def store_scores(bucket_name, filename):
    """
    Calculate scores from tweets in json object and save to Firestore.

    Parameters:
        bucket_name (str): Name of the bucket in which the object is created
        filename (str): Name of the file object
    """

    # initialize cloud storage client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    tweets = json.loads(blob.download_as_bytes())

    # initialize firestore client
    db = firestore.Client()
    collection_ref = db.collection(u'wordle_scores')

    print("Calculating scores")
    
    # each entry will have a tweetId, authorId, and tweet
    for entry in tweets:
        tweet_id = entry['tweetId']
        author_id = entry['authorId']
        tweet = entry['tweet']

        tweet = tweet.lower()
        terms = tweet.split(' ')

        try:
            round_id = terms[1]
            attempts = terms[2].split('/')[1]
            score = calculate_score(attempts)

            collection_ref.add({
                u'round_id': round_id,
                u'author_id': author_id,
                u'score': score,
                u'tweet_id': tweet_id
            })

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Encountered error {e}")

    print("Saved scores to Firestore")


def calculate_score(attempts):
    """
    Calculate score based on # of attempts.
    If failed to complete (attempt = X), then score = 0
    If completed in 1 attempt, then score = 6

    Parameters:
        attempts (string): Number of attempts

    Returns: 
        The score based on the number of attempts

    Exception:
        ValueError: when the attempts is out of bounds
    """

    score = 0
    if not attempts.isdigit():
        return score

    attempts = int(attempts)
    if attempts > 0 and attempts <= 6:
        score = 6 - attempts + 1
    else:
        raise ValueError(f'Score of {attempts} is invalid')

    return score
