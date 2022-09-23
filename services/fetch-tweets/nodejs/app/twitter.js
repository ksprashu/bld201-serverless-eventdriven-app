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

const TWITTER_V2_API = 'https://api.twitter.com/2';
const RECENT_TWEETS = '/tweets/search/recent';
const SEARCH_TERM = 'wordle -ES -is:retweet -"bopomofogame.com" -9101'

const secret = require('./secret');
const axios = require('axios').default;
const client = axios.create({
    baseURL: TWITTER_V2_API
});

/**
 * Main Call to fetch wordle tweets and and return json documents
 * @param {int} newestId the last fetched tweet id
 * @return {Promise<JSON>} a JSON document of tweets and usernames 
 */
async function getWordleTweets(newestId) {
    console.log(`Fetching tweets newer than ${newestId}`);
    
    let response = {};
    let data = await _fetchAllTweets(newestId);

    if (data && 'tweets' in data && data.tweets.length > 0) {
        response['tweets'] = _filterRelevantTweets(data.tweets);
        response['users'] = _getUsersAsMap(data.users);
        response['meta'] = data.meta;
        response.meta.filteredCount = response.tweets.length;

        console.log(`${response.meta.filteredCount} tweets prepared for save`);
        return response;        
    } else {
        console.log('No tweets fetched');
        return null;
    }
}

/**
 * Fetch all tweets that are newer than specified tweet, in batches
 * @param {string} sinceId The Id of the most recently fetched tweet
 * @return {Promise<JSON>} a JSON document of tweets and usernames 
 */
async function _fetchAllTweets(sinceId = null) {
    console.log('Recursively fetching tweets');
    let bearerToken = await secret.getTwitterBearerToken();
    let data = {};
    data['meta'] = {};
    let attempts = 1;

    try {
        let response = await _searchRecentTweets(bearerToken, sinceId, null);
        if (response.meta.result_count > 0) {
            data['tweets'] = response.data;
            data['users'] = response.includes.users;
            data['meta']['resultCount'] = response.meta.result_count;
            data['meta']['newestId'] = response.meta.newest_id;
        }

        while ('next_token' in response.meta && attempts < process.env.TWITTER_API_RATE_LIMIT) {
            response = await _searchRecentTweets(bearerToken, null, response.meta.next_token);
            if (response.meta.result_count > 0) {
                data['tweets'].push(...response.data);
                data['users'].push(...response.includes.users);
                data['meta']['resultCount'] += response.meta.result_count;
                attempts += 1;
            }
        }
    } catch (error) {
        console.warn('Exiting batch process');
        console.log(error.response.data);
        return data;
    }
    
    console.log(`Fetched ${data.meta.resultCount} total tweets`);
    return data;
}

/** 
 * Makes a HTTP call to the twitter API to get the latest tweets 
 * @param {string} bearerToken token for authentication
 * @param {int} sinceId last fetched tweet id
 * @param {string} nextToken pagination token to fetch next page
 * @return {Promise<JSON>} response from API
 */ 
async function _searchRecentTweets(bearerToken, sinceId = null, nextToken = null) {
    console.log('Fetching tweets via API');
    let params = {
        'query': SEARCH_TERM,
        'expansions': 'author_id',
        'user.fields': 'username,profile_image_url,name',
        'sort_order': 'recency',
        'max_results': process.env.TWITTER_API_MAX_RESULTS
    };

    if (sinceId) {
        params['since_id'] = sinceId;
        console.log(`Fetching tweets since ${sinceId}`);
    } else if(nextToken) {
        params['next_token'] = nextToken;
        console.log(`Fetching next page of tweets with token ${nextToken}`);
    }

    try {
        const resp = await client({
            method: 'get',
            url: RECENT_TWEETS,
            params: params,
            headers: {
                'authorization': `Bearer ${bearerToken}`
            }
        });

        // success response
        if (resp.status == 200) {
            console.log(`Fetched ${resp.data.meta.result_count} tweets from 
                ${resp.data.meta.newest_id} to ${resp.data.meta.oldest_id}`);
            return resp.data;
        } else {
            console.warn(`API returned response code: ${resp.status}`);
            throw new Error('API Call Failed');
        }
    } catch (error) {
        console.log(`API call failed with status ${error.response.status} - ${error.response.statusText}`);
        throw error;
    }
}

/**
 * Check that the tweets have the required template for wordle scores 
 * The format is expected to be "Wordle ddd d/6"
 * @param {Array} tweets 
 * @returns {Array} list of filtered tweets
 */
function _filterRelevantTweets(tweets) {
    const regex = /[Ww]ordle\s\d{2,4}\s[\dXx]\/6/g;
    let relevantTweets = [];
    for(let tweet of tweets) {
        let match = tweet.text.match(regex);
        if (match) {
            relevantTweets.push({
                'tweetId': tweet.id,
                'authorId': tweet.author_id,
                'tweet': match[0]
            });
        }
    }

    console.log(`Filtered and retained ${relevantTweets.length} relevant tweets`);
    return relevantTweets;
}

/**
 * create a user dictionary from the list
 * @param {Array} users 
 * @returns {Map} mapping of user_id to username
 */
function _getUsersAsMap(users) {
    let usernames = {};
    for(let user of users) {
        usernames[user.id] = {
            'username': user.username,
            'name': user.name,
            'profile_image_url': user.profile_image_url
        }
    }

    console.log(`Coverted ${Object.keys(usernames).length} usernames to map`);
    return usernames;
}

module.exports = {
    getWordleTweets: getWordleTweets
};
