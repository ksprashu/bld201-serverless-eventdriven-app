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

const {Storage} = require('@google-cloud/storage');
const storage = new Storage();

const TWEET_FILE_PREFIX = 'tweets';
const USER_FILE_PREFIX = 'users';

/**
* Save the list of tweets in a storage bucket
* @param {*} tweets 
*/
async function saveTweets(tweets, timestamp) {
    console.log('Saving tweets');
    try {
        let filename = [TWEET_FILE_PREFIX, timestamp.toString()].join('-');
        filename += '.json';
        let bucketname = [process.env['PROJECT_ID'], TWEET_FILE_PREFIX].join('_');
        let data = JSON.stringify(tweets);
        await storage.bucket(bucketname).file(filename).save(data);
        console.log('Tweets saved');
    } catch (error) {
        console.log(`Save failed with error - ${error.message}`);
    }
}

/**
* Save the list of users in a storage bucket
* @param {*} users 
*/
async function saveUsers(users, timestamp) {
    console.log('Saving users');
    try {
        let filename = [USER_FILE_PREFIX, timestamp.toString()].join('-');
        filename += '.json';
        let bucketname = [process.env['PROJECT_ID'], USER_FILE_PREFIX].join('_');
        let data = JSON.stringify(users);
        await storage.bucket(bucketname).file(filename).save(data);
        console.log('Users saved');
    }  catch (error) {
        console.log(`Save failed with error - ${error.message}`);
    }  
}

module.exports = {
    saveTweets: saveTweets,
    saveUsers: saveUsers
};
