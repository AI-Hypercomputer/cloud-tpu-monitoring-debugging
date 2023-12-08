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

import logging
import signal
import threading
import time

from cloud_tpu_diagnostics.src.stack_trace import disable_stack_trace_dumping
from cloud_tpu_diagnostics.src.stack_trace import enable_stack_trace_dumping

# flag to signal daemon thread to exit gracefully
_exit_flag = threading.Event()
_exit_flag.clear()
_daemon_thread = None
logger = logging.getLogger(__name__)


def start_debugging(debug_config):
  """Context manager to debug and identify errors."""
  global _daemon_thread
  _exit_flag.clear()
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    _daemon_thread = threading.Thread(
        target=send_user_signal,
        daemon=True,
        args=(debug_config.stack_trace_config.stack_trace_interval_seconds,),
    )
    _daemon_thread.start()  # start a daemon thread
    enable_stack_trace_dumping(debug_config.stack_trace_config)


def stop_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    _exit_flag.set()
    # wait for daemon thread to complete
    if _daemon_thread is not None:
      logger.info(
          "Waiting for completion of stack trace collection daemon thread."
      )
      _daemon_thread.join()
      logger.info("Stack trace collection daemon thread completed.")
    disable_stack_trace_dumping(debug_config.stack_trace_config)
  _exit_flag.clear()


def send_user_signal(stack_trace_interval_seconds):
  """Send SIGUSR1 signal to main thread after every stack_trace_interval_seconds seconds."""
  while not _exit_flag.is_set():
    time.sleep(stack_trace_interval_seconds)
    if not _exit_flag.is_set():
      signal.pthread_kill(threading.main_thread().ident, signal.SIGUSR1)
