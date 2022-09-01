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

// Import the Secret Manager client and instantiate it:
const {SecretManagerServiceClient} = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

/**
* Get the twitter bearer token
* @return {Promise<string>} bearer token for accessing twitter API
*/
async function getTwitterBearerToken() {
  console.log('Getting secret');
  
  const BEARER_TOKEN_NAME = 'projects/266838624898/secrets/twitter-dev-bearer-token/versions/latest';
  const [secretResponse] = await client.accessSecretVersion({
    name: BEARER_TOKEN_NAME
  });
  
  console.log('Secret fetched');
  // Extract the payload as a string.
  return secretResponse.payload.data.toString();
}

module.exports = {
  getTwitterBearerToken: getTwitterBearerToken
};
