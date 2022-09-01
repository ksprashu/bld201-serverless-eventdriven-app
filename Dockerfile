# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use the official lightweight Node.js 12 image.
# https://hub.docker.com/_/node
FROM node:18-slim

WORKDIR /usr/src/app
COPY package*.json ./

# Install dependencies.
RUN npm ci --only=production

# Copy local code to the container image.
COPY . ./
RUN mkdir -p /usr/src/app/app
COPY ./app/* ./app/

# Run the web service on container startup.
CMD ["npm", "start"]