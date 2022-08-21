const TWITTER_V2_API = 'https://api.twitter.com/2';
const RECENT_TWEETS = '/tweets/search/recent'

const axios = require('axios').default;
const client = axios.create({
    baseURL: TWITTER_V2_API
});

async function searchRecentTweets() {
    const resp = await client({
        method: 'get',
        url: RECENT_TWEETS,
        params: {
            'query': 'wordle',
            'expansions': 'author_id',
            'user.fields': 'username',
            'max_results': 100
        },
        headers: {
            'authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`
        }
    });

    if (resp.status == 200) {
        return resp.data;
    } else {
        throw new Error('API Call Failed');
    }
}

async function getWordleTweets(data) {
    return Promise.all([
        _filterRelevantTweets(data.data), 
        _parseUsernames(data.includes.users)])
        .then(([filteredTweets, usernames]) => {
            return _addUsernameToTweets(filteredTweets, usernames);
        });
}

async function _filterRelevantTweets(tweets) {
    const regex = /[Ww]ordle\s\d{2,4}\s[\dXx]\/6/g;
    let relevantTweets = [];
    for(let tweet of tweets) {
        let match = tweet.text.match(regex);
        if (match) {
            relevantTweets.push({
                author_id: tweet.author_id,
                wordle_tweet: match[0]
            });
        }
    }

    return relevantTweets;
}

async function _parseUsernames(users) {
    let usernames = {}
    for(let user of users) {
        usernames[user.id] = user.username;
    }

    return usernames;
}

async function _addUsernameToTweets(tweets, usernames) {
    for (let tweet of tweets) {
        tweet['username'] = usernames[tweet.author_id];
    }
    return tweets;
}

module.exports = {
    searchRecentTweets: searchRecentTweets,
    getWordleTweets: getWordleTweets
};
