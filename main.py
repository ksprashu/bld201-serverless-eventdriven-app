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
    store_usernames(bucket_name, filename)


def store_usernames(bucket_name, filename):
    """
    Store usernames from json file in a Storage bucket, into Firestore

    Parameters:
        bucket_name (str): Name of the bucket in which the object is created
        filename (str): Name of the file object
    """

    # initialize cloud storage client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    usernames = json.loads(blob.download_as_bytes())

    # initialize firestore client
    db = firestore.Client()
    collection_ref = db.collection(u'users')

    print("Updating user entries in firestore")

    # usernames will be a map of id: username
    for userid, username in usernames.items():
        collection_ref.document(str(userid)).set({
            u'userid': userid,
            u'username': username
        })
