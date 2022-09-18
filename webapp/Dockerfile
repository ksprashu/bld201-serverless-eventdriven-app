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

# develop stage
FROM node:18 as build-stage
WORKDIR /app
COPY package*.json ./
RUN yarn global add @quasar/cli
RUN yarn
RUN yarn quasar build
COPY . .

# build stage
# FROM develop-stage as build-stage
# RUN yarn
# RUN quasar build

# production stage
FROM node:18 as production-stage
WORKDIR /app
COPY --from=build-stage /app/dist/spa .
RUN yarn global add @quasar/cli
CMD ["yarn", "quasar", "serve"]
