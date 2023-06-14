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

from unittest import mock
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import debug_configuration
from cloud_tpu_diagnostics.src.config import diagnostic_configuration
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.diagnose import diagnose


class DiagnoseTest(absltest.TestCase):

  @mock.patch(
      'google3.third_party.cloud_tpu_monitoring_debugging.pip_package.cloud_tpu_diagnostics.src.diagnose.start_debugging'
  )
  @mock.patch(
      'google3.third_party.cloud_tpu_monitoring_debugging.pip_package.cloud_tpu_diagnostics.src.diagnose.stop_debugging'
  )
  def testDiagnoseContextManager(
      self, stop_debugging_mock, start_debugging_mock
  ):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=True,
        ),
    )
    diagnostic_config = diagnostic_configuration.DiagnosticConfig(
        debug_config=debug_config,
    )
    with diagnose(diagnostic_config):
      pass
    start_debugging_mock.assert_called_once_with(debug_config)
    stop_debugging_mock.assert_called_once_with(debug_config)


if __name__ == '__main__':
  absltest.main()
