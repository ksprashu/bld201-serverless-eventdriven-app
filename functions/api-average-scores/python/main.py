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

import traceback
import functions_framework
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
    return (jsonify(fetch_top_average_scores()), 200, headers)    


def fetch_top_average_scores():
    """
    Returns the top average scores from Firestore
    The data should contain userdata - username, name, profile_image_url
    and total scores. Ordered by total scores.
    """
    # initialize firestore client
    db = firestore.Client()
    user_coll = db.collection(USER_COLLECTION)

    try:
        user_docs = user_coll. \
            order_by('average_score', direction=firestore.Query.DESCENDING) \
                .order_by('max_streak', direction=firestore.Query.DESCENDING) \
                .order_by('total_score', direction=firestore.Query.DESCENDING) \
                .limit(10).stream()

        data = []
        for user_doc in user_docs:
            doc = user_doc.to_dict()
            data.append({
                u'username': doc.get('username'), 
                u'name': doc.get('name', ''),
                u'profile_image_url': doc.get('profile_image_url', ''),
                u'score': doc.get('average_score')
            })
            print(f"user {doc.get('username')} scored {doc.get('average_score')}")

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
                "username": "abc",
                "name": "abc name", 
                "profile_image_url": "https://cdn.quasar.dev/img/boy-avatar.png",
                "score": 5.5
            },
            {
                "username": "def",
                "name": "def name", 
                "profile_image_url": "https://cdn.quasar.dev/img/boy-avatar.png",
                "score": 4.4
            },
            {
                "username": "xyz",
                "name": "xyz name", 
                "profile_image_url": "https://cdn.quasar.dev/img/boy-avatar.png",
                "score": 3.21
            }
        ],
        "count": 3
    }

    return response
