Drone-Netlify
========
Provide preview for harvester/docs, support PR to show preview information for Drone CI

## Settings
Drone-Netlify is uses environment variables to set.


#### <a id="NETLIFY_AUTH_TOKEN">NETLIFY_AUTH_TOKEN</a>
 * type: `string`
 * require: `true`

#### <a id="NETLIFY_SITE_ID">NETLIFY_SITE_ID</a>
 * type: `string`
 * require: `true`

#### <a id="GITHUB_TOKEN">GITHUB_TOKEN</a>
 * type: `string`
 * require: `true`

#### <a id="DRONE_REPO">DRONE_REPO</a>
 * type: `string`
 * require: `true`
 * example: `https://github.com/harvester/docs`

#### <a id="DRONE_PULL_REQUEST">DRONE_PULL_REQUEST</a>
 * type: `string`
 * require: `true`

Using pull request number to get information.

#### <a id="DRONE_COMMIT">DRONE_COMMIT</a>
 * type: `string`
 * require: `true`

#### <a id="BUILD_ZIP_FILE">BUILD_ZIP_FILE</a>
 * type: `string`
 * require: `false`
 * default: `build.zip`




## License
Copyright (c) 2023 [Rancher Labs, Inc.](http://rancher.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.