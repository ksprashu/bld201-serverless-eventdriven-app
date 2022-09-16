// Copyright 2022 Google LLC

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     https://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const {Firestore} = require('@google-cloud/firestore');
const METADATA_COLLECTION = 'fetch_metadata';
const LATEST_DOCID = 'latest';

/**
* Get the most recently fetched tweet id from firestore
* @return {Promise<string>} the Id of the most recently fetched tweet
*/
async function getMostRecentTweetId() {
    console.log('Fetching latest tweet id');
    
    const firestore = new Firestore();
    const collectionRef = firestore.collection(METADATA_COLLECTION).doc(LATEST_DOCID);
    const doc = await collectionRef.get();
    
    if (!doc.exists || !(doc.get('newestId'))) {
        console.warn('No fetch metadata');
        return null;
    } else {
        console.log(`Last fetched tweet: ${doc.get('newestId')}`);
        return doc.get('newestId');
    }
}

/**
* Update the latest fetch data and fetch history
* @param {Map} metadata Map of latest fetched tweet id, and result count
*/
async function updateMostRecentTweetId(metadata) {
    console.log('Saving latest tweet id');
    
    const firestore = new Firestore();
    const data = {
        'newestId': metadata.newestId,
        'timestamp': Date.now(),
        'resultCount': metadata.resultCount
    };
    
    try {
        // create a doc with 'timestamp' for recording history
        // await firestore.collection(METADATA_COLLECTION).doc(data.timestamp.toString()).set(data);
        // create a document called 'latest' for faster fetch
        await firestore.collection(METADATA_COLLECTION).doc(LATEST_DOCID).set(data);       
        console.log('Saved tweet metadata');
    } catch (error) {
        console.warn(`Data save failed with error ${error.message}`);
    }
}

module.exports = {
    getMostRecentTweetId: getMostRecentTweetId,
    updateMostRecentTweetId: updateMostRecentTweetId
};
