require('dotenv').config();

const twitter = require('./twitter')
twitter.searchRecentTweets()
    .then((data) => twitter.getWordleTweets(data))
    .then((data) => console.log(data.length)) 

// const secret = require('./secret');
// secret.displaySecrets();

