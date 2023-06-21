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

import faulthandler
import os
import shutil
import signal
import subprocess
import sys
import textwrap
import unittest
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.stack_trace import disable_stack_trace_dumping
from cloud_tpu_diagnostics.src.stack_trace import enable_stack_trace_dumping
from cloud_tpu_diagnostics.src.util import default

class StackTraceTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    package_dir = '/'.join(os.path.dirname(__file__).split('/')[:-1])
    # Used to run test with blaze/bazel
    self.test_binary = os.path.join(package_dir, 'stack_trace_test_util')
    # Used to run test with unittest `python3 -m unittest stack_trace_test.py`
    self.test_file = os.path.join(
        package_dir, 'src/util/stack_trace_test_util.py'
    )

  def tearDown(self):
    super().tearDown()
    if os.path.exists(default.STACK_TRACE_DIR_DEFAULT):
      shutil.rmtree(default.STACK_TRACE_DIR_DEFAULT)

  @unittest.skipIf(not hasattr(signal, 'SIGSEGV'), 'Missing signal.SIGSEGV')
  def testSigsegvCollectStackTraceTrueTraceCollectedOnCloud(self):
    error = 'Fatal Python error: Segmentation fault'
    self.check_fatal_error(51, error, 'SIGSEGV', True)

  @unittest.skipIf(not hasattr(signal, 'SIGABRT'), 'Missing signal.SIGABRT')
  def testSigabrtCollectStackTraceTrueTraceCollectedOnCloud(self):
    error = 'Fatal Python error: Aborted'
    self.check_fatal_error(54, error, 'SIGABRT', True)

  @unittest.skipIf(not hasattr(signal, 'SIGFPE'), 'Missing signal.SIGFPE')
  def testSigfpeCollectStackTraceTrueTraceCollectedOnCloud(self):
    error = 'Fatal Python error: Floating point exception'
    self.check_fatal_error(57, error, 'SIGFPE', True)

  @unittest.skipIf(not hasattr(signal, 'SIGILL'), 'Missing signal.SIGILL')
  def testSigillCollectStackTraceTrueTraceCollectedOnCloud(self):
    error = 'Fatal Python error: Illegal instruction'
    self.check_fatal_error(60, error, 'SIGILL', True)

  @unittest.skipIf(not hasattr(signal, 'SIGBUS'), 'Missing signal.SIGBUS')
  def testSigbusCollectStackTraceTrueTraceCollectedOnCloud(self):
    error = 'Fatal Python error: Bus error'
    self.check_fatal_error(63, error, 'SIGBUS', True)

  @unittest.skipIf(not hasattr(signal, 'SIGUSR1'), 'Missing signal.SIGUSR1')
  def testSigusrCollectStackTraceTrueTraceCollectedOnCloud(self):
    self.check_fatal_error(66, '', 'SIGUSR1', True)

  def testNoFaultCollectStackTraceTrueNoTraceCollectedOnCloud(self):
    output, stderr = self.get_output('', True, True)
    self.assertEqual(output, '')
    self.assertEqual(stderr, '')

  def testCollectStackTraceFalseNoTraceDirCreated(self):
    process = self.run_python_code('', False, True)
    _, stderr = process.communicate()
    self.assertFalse(os.path.exists(default.STACK_TRACE_DIR_DEFAULT))
    self.assertEmpty(stderr)

  @unittest.skipIf(not hasattr(signal, 'SIGUSR1'), 'Missing signal.SIGUSR1')
  def testCollectStackTraceToConsole(self):
    self.check_fatal_error(66, '', 'SIGUSR1', False)

  def testNoFaultCollectStackTraceTrueNoTraceCollectedOnConsole(self):
    output, stderr = self.get_output('', True, False)
    self.assertEqual(output, '')
    self.assertEqual(stderr, '')

  def testCollectStackTraceFalseNoTraceCollectedOnConsole(self):
    process = self.run_python_code('', False, False)
    _, stderr = process.communicate()
    self.assertEmpty(stderr)
    self.assertFalse(os.path.exists(default.STACK_TRACE_DIR_DEFAULT))

  def testEnableStackTraceDumpingFaulthandlerEnabled(self):
    stack_trace_config = stack_trace_configuration.StackTraceConfig(
        collect_stack_trace=True, stack_trace_to_cloud=True
    )
    with self.assertLogs(level='INFO') as log:
      enable_stack_trace_dumping(stack_trace_config)
    self.assertEqual(faulthandler.is_enabled(), True)
    self.assertRegex(
        log.output[0], 'Stack trace will be written in: /tmp/debugging/'
    )

  def testDisableStackTraceDumpingFaulthandlerDisabled(self):
    stack_trace_config = stack_trace_configuration.StackTraceConfig(
        collect_stack_trace=True, stack_trace_to_cloud=True
    )
    enable_stack_trace_dumping(stack_trace_config)
    disable_stack_trace_dumping(stack_trace_config)
    self.assertEqual(faulthandler.is_enabled(), False)

  def check_fatal_error(self, line_number, error, signal_name, log_to_cloud):
    header = r'Stack \(most recent call first\)'
    regex = ''
    if error:
      regex = """
          {error}
          """
    regex += """
          {header}:
            File "{filename}", line {line_number} in <module>
          """
    regex = (
        textwrap.dedent(regex)
        .format(
            error=error,
            header=header,
            filename=self.test_file,
            line_number=line_number,
        )
        .strip()
    )

    output, stderr = self.get_output(signal_name, True, log_to_cloud)
    if log_to_cloud:
      self.assertRegex(output, regex)
      self.assertEmpty(stderr)
    else:
      self.assertRegex(stderr, regex)
      self.assertEmpty(output)

  def get_output(self, signal_name, collect_stack_trace, log_to_cloud):
    process = self.run_python_code(
        signal_name, collect_stack_trace, log_to_cloud
    )
    _, stderr = process.communicate()
    stderr = stderr.decode('ascii', 'backslashreplace')
    output = ''
    if log_to_cloud:
      trace_file = os.listdir(default.STACK_TRACE_DIR_DEFAULT)
      if trace_file:
        stack_trace_file = default.STACK_TRACE_DIR_DEFAULT + trace_file[0]
        with open(stack_trace_file, 'rb') as fp:
          output = fp.read().decode('ascii', 'backslashreplace')
    return output, stderr

  def run_python_code(self, signal_name, collect_stack_trace, log_to_cloud):
    args = [
        '--signal=' + signal_name,
        '--collect_stack_trace=' + str(collect_stack_trace),
        '--log_to_cloud=' + str(log_to_cloud),
    ]
    if sys.executable is not None:
      code = [sys.executable, self.test_file]
    else:
      code = [self.test_binary]
    return subprocess.Popen(
        code + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )


if __name__ == '__main__':
  absltest.main()
