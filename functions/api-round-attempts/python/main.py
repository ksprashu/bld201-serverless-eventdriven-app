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
from google.cloud import firestore
from flask import jsonify

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
    return jsonify(fetch_per_round_best_attempt())


def fetch_per_round_best_attempt():
    """
    Returns the best attempts for each round from Firestore
    The data should contain round information - round number, and score
    and number of users that solved in this many attempts
    Ordered by latest round first.
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
