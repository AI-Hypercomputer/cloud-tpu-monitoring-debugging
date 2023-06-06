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

import threading
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import debug_configuration
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.debug import start_debugging


class DebugTest(absltest.TestCase):

  def testDaemonThreadRunningWhenCollectStackTraceTrue(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 2)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 1)

  def testDaemonThreadNotRunningWhenCollectStackTraceFalse(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=False,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 1)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 0)


if __name__ == '__main__':
  absltest.main()
