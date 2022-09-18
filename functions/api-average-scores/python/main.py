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
    return jsonify(fetch_top_average_scores())


def fetch_top_average_scores():
    """
    Returns the top average scores from Firestore
    The data should contain userdata - username, name, profile_image_url
    and total scores. Ordered by total scores.
    """

    response = {
        "data": [
            {
                "userdata": {"abc", "abc name", 
                    "https://cdn.quasar.dev/img/boy-avatar.png"},
                "score": 5.5
            },
            {
                "userdata": {"def", "def name", 
                    "https://cdn.quasar.dev/img/boy-avatar.png"},
                "score": 4.4
            },
            {
                "userdata": {"xyz", "xyz name", 
                    "https://cdn.quasar.dev/img/boy-avatar.png"},
                "score": 3.21
            }
        ],
        "count": 3
    }

    return response

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
    return fetch_top_average_scores()


def fetch_top_average_scores():
    """
    Returns the top average scores from Firestore
    The data should contain userdata - username, name, profile_image_url
    and total scores. Ordered by total scores.
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
