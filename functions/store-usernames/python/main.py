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

from heapq import merge
import functions_framework
import json

from google.cloud import storage
from google.cloud import firestore

USER_COLLECTION = u'users'


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
    collection_ref = db.collection(USER_COLLECTION)

    print("Updating user entries in firestore")

    # usernames will be a map of id: username
    for userid, userdata in usernames.items():
        user_doc = {
            u'userid': str(userid),
            u'username': str(userdata['username']),
            u'name': str(userdata.get('name', '')),
            u'profile_image_url': str(userdata.get('profile_image_url',''))
        }

        check_and_update_userdata(collection_ref, user_doc)           

    print("User data updated")


def check_and_update_userdata(coll_ref, user_doc):
    """
    Checks whether the user data need to be updated or created.

    Parameters:
        coll_ref (Object): Reference to users collection
        user_doc (Object): The user data that needs to be updated
    """

    doc = coll_ref.document(user_doc['userid']).get()
    if not doc.exists:
        coll_ref.document(user_doc['userid']).set(user_doc)
        print(f"user {user_doc['userid']} created")
    else:
        coll_ref.document(user_doc['userid']).set(user_doc, merge=True)
