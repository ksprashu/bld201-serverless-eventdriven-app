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

const firestore = require('./app/firestore');
const storage = require('./app/storage');
const twitter = require('./app/twitter');

require('dotenv').config();

// Running express listener as required by cloud run contract
const express = require('express');
const app = express();

const port = parseInt(process.env.PORT) || 8080;
app.listen(port, () => {
  console.log(`helloworld: listening on port ${port}`);
});

/**
 * Main function
 */
async function fetchTweetsAndSave() {
    console.log('Starting new run');
    let newestId = await firestore.getMostRecentTweetId();
    let response = await twitter.getWordleTweets(newestId);
    if (response) {
        await storage.saveTweets(response.tweets);
        await storage.saveUsers(response.users);
        await firestore.updateMostRecentTweetId(response.meta);
    }
    console.log('Run complete');
}

app.get('/', (req, res) => {
    fetchTweetsAndSave();
    res.send(`Tweet fetch process triggered!`);
});


