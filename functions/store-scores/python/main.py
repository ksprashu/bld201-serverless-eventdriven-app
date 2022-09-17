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

    print("Initializing clients to save scores")

    # initialize cloud storage client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    tweets = json.loads(blob.download_as_bytes())

    # initialize firestore client
    db = firestore.Client()
    collection_ref = db.collection(u'wordle_scores')

    print("Calculating and saving scores")
    
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
            score_doc = {
                u'round_id': round_id,
                u'author_id': author_id,
                u'score': score,
                u'tweet_id': tweet_id
            }
            write_or_update_score(collection_ref, score_doc)

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Encountered error {e}")

    print("Saved scores to Firestore")


def write_or_update_score(coll_ref, score_doc):
    """
    Update the user's score for the given round if already present, or 
    create a new score entry for a new round. A user should have only 1 score
    per round. We will default to the lowest score (highest attempts).

    Parameters:
        coll_ref (Object): An instance of the score collection in Firestore
        score_doc (Object): A dictionary of score, round_id, author_id, tweet_id

    Return:
        Boolean indicating success or failure 
    """

    score_docs = coll_ref.where(u'round_id', u'==', score_doc['round_id']) \
        .where(u'author_id', u'==', score_doc['author_id']).get()

    if len(score_docs) == 0:
        coll_ref.add(score_doc)
        print(f"Wrote new entry for author = {score_doc['author_id']} \
            for round {score_doc['round_id']}")
    elif len(score_docs) > 1:
        raise ValueError(f'Found {len(score_docs)} entries \
            for round - {score_doc["round_id"]} \
            for player - {score_doc["author_id"]}')
    else:
        # update the scores for this record
        print(f"Score exists for author {score_doc['author_id']} \
            for round {score_doc['round_id']}")
        old_score_doc = score_docs[0]
        coll_ref.document(old_score_doc.id).set(score_doc)
        print(f"Updated existing entry with id {old_score_doc.id}")


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
