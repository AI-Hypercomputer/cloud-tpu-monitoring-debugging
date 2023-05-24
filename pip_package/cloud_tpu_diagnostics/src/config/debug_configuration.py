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
from typing import Optional
from cloud_tpu_diagnostics.src.config import stack_trace_configuration


@dataclasses.dataclass
class DebugConfig:
  """Configuration for debugging.

  Attributes:
    stack_trace_config: config object for stack trace collection, default is
      None
  """

  stack_trace_config: Optional[stack_trace_configuration.StackTraceConfig] = (
      None
  )
