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

import functions_framework
import json

from google.cloud import storage
from google.cloud import firestore

METADATA_COLLECTION = u'metadata'
SCORE_COLLECTION = u'scores'
USER_COLLECTION = u'users'
ROUND_DOCID = u'rounds'

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

    latest_round = 0
    print("Calculating and saving scores")
    
    # each entry will have a tweetId, authorId, and tweet
    for entry in tweets:
        tweetid = entry['tweetId']
        userid = entry['authorId']
        tweet = entry['tweet']

        tweet = tweet.lower()
        terms = tweet.split(' ')

        try:
            roundid = int(terms[1])
            attempts = terms[2].split('/')[1]
            score = calculate_score(attempts)
            score_doc = {
                u'roundid': roundid,
                u'userid': userid,
                u'score': score,
                u'attempts': attempts,
                u'tweetid': tweetid
            }

            # keep track of the latest round
            if roundid > latest_round:
                latest_round = roundid

            write_and_update_score(db, score_doc)
            update_round_metadata(db, latest_round)

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Encountered error {e}")

    print("Saved scores to Firestore")


def update_round_metadata(db, latest_round): 
    """
    Updates the metadata with latest round scored

    Parameters:
        db (Object): An instance of the Firestore client
        latest_round (int): Value of the latest round fetched
    """
    round_ref = db.collection(METADATA_COLLECTION).document(ROUND_DOCID)
    round_doc = round_ref.get()
    if round_doc.exists:
        current_latest = round_doc.get(u'latest_round')
        if latest_round > current_latest:
            round_ref.set({
                u'latest_round': latest_round
            }, merge=True)
    else:
        round_ref.set({
            u'latest_round': latest_round
        })
    print(f'latest round updated to {latest_round}')


def write_and_update_score(db, score_doc):
    """
    If the user's score is already present, then ignore the new score / tweet.
    When writing a new score, then update the users average. 

    Parameters:
        db (Object): An instance of the Firestore client
        score_doc (Object): A dictionary of score, roundid, userid, tweetid

    Return:
        Boolean indicating success or failure 
    """

    score_coll_ref = db.collection(SCORE_COLLECTION)
    score_docs = score_coll_ref.where(u'roundid', u'==', score_doc['roundid']) \
        .where(u'userid', u'==', score_doc['userid']).get()

    if len(score_docs) == 0:
        score_coll_ref.add(score_doc)
        print(f"Wrote new entry for author = {score_doc['userid']} \
            for round {score_doc['roundid']}")

        doc_ref = db.collection(USER_COLLECTION).document(score_doc['userid'])
        doc = doc_ref.get()
        if doc.exists:
            user_doc = doc.to_dict()
            current_score = score_doc['score']
            
            rounds_played = user_doc.get('rounds_played', 0)
            user_doc[u'rounds_played'] = rounds_played + 1

            average_score = user_doc.get('average_score', 0)
            average_score = (average_score * rounds_played + current_score) \
                / (rounds_played + 1)
            user_doc[u'average_score'] = average_score

            total_score = user_doc.get('total_score', 0)
            user_doc[u'total_score'] = total_score + current_score
            
            current_streak = user_doc.get('current_streak', 0)
            current_streak = current_streak + 1 if current_score > 0 else 1
            user_doc[u'current_streak'] = current_streak

            max_streak = user_doc.get('max_streak', 0)
            user_doc[u'max_streak'] = max(max_streak, current_streak)

            doc_ref.set(user_doc, merge=True)
            print(f"Updated user {score_doc['userid']}")

        else:
            user_doc = {
                u'userid': score_doc['userid'],
                u'rounds_played': 1,
                u'average_score': score_doc['score'],
                u'total_score': score_doc['score'],
                u'max_streak': 1,
                u'current_streak': 1
            }
            doc_ref.set(user_doc)
            print(f"Created user {score_doc['userid']}")


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
