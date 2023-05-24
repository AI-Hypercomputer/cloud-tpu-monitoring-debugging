# Copyright 2023 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dataclasses
from cloud_tpu_diagnostics.src.util import default


@dataclasses.dataclass
class StackTraceConfig:
  """Configuration for stack trace collection.

  Attributes:
    collect_stack_trace: enable/disable collection of stack trace in case fault
      occurs in the program. Default is False, which means stack trace will not
      be collected unless collect_stack_trace is set to True.
    stack_trace_to_cloud: enable/disable upload of stack trace to cloud. Default
      is False, which means stack trace will be displayed on the termial unless
      stack_trace_to_cloud is set to True.
  """

  collect_stack_trace: bool = default.COLLECT_STACK_TRACE_DEFAULT
  stack_trace_to_cloud: bool = default.STACK_TRACE_TO_CLOUD_DEFAULT
