<!--
 Copyright 2023 Google LLC
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
      https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->
# Changelog

<!--

Changelog follow the https://keepachangelog.com/ standard (at least the headers)

This allow to:

* auto-parsing release notes during the automated releases from github-action:
  https://github.com/marketplace/actions/pypi-github-auto-release
* Have clickable headers in the rendered markdown

To release a new version (e.g. from `1.0.0` -> `2.0.0`):

* Create a new `# [2.0.0] - YYYY-MM-DD` header and add the changes to be released.
* At the end of the file:
  * Define the new link url:
  `[2.0.0]: https://github.com/google/cloud-tpu-monitoring-debugging/compare/v1.0.0...v2.0.0`

-->

## [0.1.3] - 2023-11-01
* Fixing issue with using signals and threads together in a program

## [0.1.2] - 2023-09-20
* Improved stack trace readability and clarity by adding a message for more information

## [0.1.1] - 2023-06-21
* Bug Fixes
  * Fixes dumping of stack traces on the console when exceptions like `AssertionError`, `tensorflow.python.framework.errors_impl.NotFoundError` are thrown when `collect_stack_trace=True` and `stack_trace_to_cloud=False`.
* Updated README

## [0.1.0] - 2023-06-08
* Initial release of cloud-tpu-diagnostics PyPI package
* FEATURE: Contains debug module to collect stack traces on faults

[0.1.3]: https://github.com/google/cloud-tpu-monitoring-debugging/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/google/cloud-tpu-monitoring-debugging/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/google/cloud-tpu-monitoring-debugging/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/google/cloud-tpu-monitoring-debugging/releases/tag/v0.1.0
