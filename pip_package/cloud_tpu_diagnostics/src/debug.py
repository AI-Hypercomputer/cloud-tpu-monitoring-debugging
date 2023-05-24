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

import signal
import threading
import time

from cloud_tpu_diagnostics.src.stack_trace import disable_stack_trace_dumping
from cloud_tpu_diagnostics.src.stack_trace import enable_stack_trace_dumping


def start_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    thread = threading.Thread(target=send_user_signal, daemon=True)
    thread.start()  # start a daemon thread
    enable_stack_trace_dumping(debug_config.stack_trace_config)


def stop_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    disable_stack_trace_dumping()


def send_user_signal():
  """Send SIGUSR1 signal to non-daemon threads after every 10 minutes."""
  while True:
    time.sleep(600)  # sleep for 10 minutes
    for thread in threading.enumerate():
      if not thread.daemon:
        signal.pthread_kill(thread.ident, signal.SIGUSR1)
