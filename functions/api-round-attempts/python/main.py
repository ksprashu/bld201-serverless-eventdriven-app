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
import traceback
from google.cloud import firestore
from flask import jsonify

METADATA_COLLECTION = u'metadata'
SCORE_COLLECTION = u'scores'
USER_COLLECTION = u'users'
ROUND_DOCID = u'rounds'

@functions_framework.http
def http_receiver(request):
    """
    HTTP Trigger called when this function is called via HTTP

    Parameters:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>
    """

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }    
    return (jsonify(fetch_per_round_best_attempt()), 200, headers)


def fetch_per_round_best_attempt():
    """
    Returns the best attempts for each round from Firestore
    The data should contain round information - round number, and score
    and number of users that solved in this many attempts
    Ordered by latest round first.
    """

    # initialize firestore client
    db = firestore.Client()
    round_ref = db.collection(METADATA_COLLECTION).document(ROUND_DOCID)
    round_doc = round_ref.get()

    if not round_doc.exists:
        return get_canned_response()

    try:
        data = []
        score_ref = db.collection(SCORE_COLLECTION)
        latest_round = round_doc.get('latest_round')
        for roundid in range(latest_round, latest_round - 20, -1):
            least_attempt_doc = score_ref \
                .where(u'roundid', u'==', roundid) \
                .where(u'attempts', u'>', 0) \
                .order_by(u'attempts') \
                .limit(1) \
                .get()
            
            best_attempt = least_attempt_doc['attempts']
            best_attempt_count = 0
            if len(least_attempt_doc) != 1:
                print(f"No attempts for round {roundid}!!!")
            else:
                attempts_docs = score_ref \
                    .where(u'roundid', u'==', roundid) \
                    .where(u'attempts', u'==', best_attempt) \
                    .stream()
                best_attempt_count = len(list(attempts_docs))

            data.append({
                u'roundid': roundid,
                u'best_attempt': best_attempt,
                u'user_count': best_attempt_count
            })
            print(f"Best attempt = {best_attempt} for round {roundid}")

        return {
            "data": data,
            "count": len(data)
        }
    except Exception as e:
        print(f"Encountered error {e}")
        traceback.print_exc()
        return get_canned_response()


def get_canned_response():
    """
    Static json for respose format and as a backup.
    """
    response = {
        "data": [
            {
                "roundid": 455,
                "best_attempt": 2,
                "user_count": 4               
            },
            {
                "roundid": 454,
                "best_attempt": 1,
                "user_count": 1
            },
            {
                "roundid": 453,
                "best_attempt": 4,
                "user_count": 53
            }
        ],
        "count": 3
    }

    return response
