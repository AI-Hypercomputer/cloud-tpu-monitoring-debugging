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

import contextlib

from cloud_tpu_diagnostics.src.debug import start_debugging
from cloud_tpu_diagnostics.src.debug import stop_debugging


@contextlib.contextmanager
def diagnose(config):
  """Context manager to debug and identify errors."""
  if config is not None and config.debug_config is not None:
    start_debugging(config.debug_config)
  try:
    yield
    if config is not None and config.debug_config is not None:
      stop_debugging(config.debug_config)
  except Exception as e:
    raise e
