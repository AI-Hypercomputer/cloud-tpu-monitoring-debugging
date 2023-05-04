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

import os
import signal
import subprocess
import sys
import tempfile
import textwrap
import unittest
from absl.testing import absltest


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
    os.environ.pop('COLLECT_STACK_TRACE', None)
    os.environ.pop('STACK_TRACE_DIR', None)

  @unittest.skipIf(not hasattr(signal, 'SIGSEGV'), 'Missing signal.SIGSEGV')
  def testSigsegvCollectStackTraceTrueTraceCollected(self):
    error = 'Fatal Python error: Segmentation fault'
    self.check_fatal_error(31, error, 'SIGSEGV')

  @unittest.skipIf(not hasattr(signal, 'SIGABRT'), 'Missing signal.SIGABRT')
  def testSigabrtCollectStackTraceTrueTraceCollected(self):
    error = 'Fatal Python error: Aborted'
    self.check_fatal_error(34, error, 'SIGABRT')

  @unittest.skipIf(not hasattr(signal, 'SIGFPE'), 'Missing signal.SIGFPE')
  def testSigfpeCollectStackTraceTrueTraceCollected(self):
    error = 'Fatal Python error: Floating point exception'
    self.check_fatal_error(37, error, 'SIGFPE')

  @unittest.skipIf(not hasattr(signal, 'SIGILL'), 'Missing signal.SIGILL')
  def testSigillCollectStackTraceTrueTraceCollected(self):
    error = 'Fatal Python error: Illegal instruction'
    self.check_fatal_error(40, error, 'SIGILL')

  @unittest.skipIf(not hasattr(signal, 'SIGBUS'), 'Missing signal.SIGBUS')
  def testSigbusCollectStackTraceTrueTraceCollected(self):
    error = 'Fatal Python error: Bus error'
    self.check_fatal_error(43, error, 'SIGBUS')

  @unittest.skipIf(not hasattr(signal, 'SIGUSR1'), 'Missing signal.SIGUSR1')
  def testSigusrCollectStackTraceTrueTraceCollected(self):
    self.check_fatal_error(46, '', 'SIGUSR1')

  def testNoFaultCollectStackTraceTrueNoTraceCollected(self):
    trace_dir = tempfile.mkdtemp()
    self.set_env_variables(trace_dir)
    output = self.get_output('', trace_dir)
    self.assertEqual(output, '')

  def testCollectStackTraceFalseNoTraceDirCreated(self):
    trace_dir = tempfile.mkdtemp()
    process = self.run_python_code('', trace_dir)
    _, _ = process.communicate()
    self.assertEmpty(os.listdir((trace_dir)))

  def testInvalidCollectStackTraceSetValueError(self):
    os.environ['COLLECT_STACK_TRACE'] = 'rue'
    trace_dir = tempfile.mkdtemp()
    process = self.run_python_code('', trace_dir)
    _, stderr = process.communicate()
    self.assertNotEmpty(stderr)

  def testStackTraceDirUnsetTraceCollectedInDefaultDir(self):
    os.environ['COLLECT_STACK_TRACE'] = 'True'
    trace_dir = tempfile.mkdtemp()
    process = self.run_python_code('', trace_dir)
    _, _ = process.communicate()
    self.assertEmpty(os.listdir((trace_dir)))
    self.assertTrue(os.path.isdir('/tmp/debugging'))

  def testStackTraceDirNotPresentTraceNotCollected(self):
    os.environ['COLLECT_STACK_TRACE'] = 'True'
    os.environ['STACK_TRACE_DIR'] = '/test'
    trace_dir = tempfile.mkdtemp()
    process = self.run_python_code('', trace_dir)
    _, stderr = process.communicate()
    self.assertNotEmpty(stderr)
    self.assertFalse(os.path.isdir('/test/debugging'))

  def check_fatal_error(self, line_number, error, signal_name):
    header = r'Current thread 0x[0-9a-f]+ \(most recent call first\)'
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

    trace_dir = tempfile.mkdtemp()
    self.set_env_variables(trace_dir)
    output = self.get_output(signal_name, trace_dir)
    self.assertRegex(output, regex)

  def set_env_variables(self, trace_dir):
    os.environ['COLLECT_STACK_TRACE'] = 'True'
    os.environ['STACK_TRACE_DIR'] = trace_dir

  def get_output(self, signal_name, trace_dir):
    process = self.run_python_code(signal_name, trace_dir)
    _, _ = process.communicate()
    trace_file = os.listdir(trace_dir + '/debugging')
    output = ''
    if trace_file:
      stack_trace_file = trace_dir + '/debugging/' + trace_file[0]
      with open(stack_trace_file, 'rb') as fp:
        output = fp.read().decode('ascii', 'backslashreplace')
    return output

  def run_python_code(self, signal_name, trace_dir):
    args = ['--signal=' + signal_name, '--trace_dir=' + trace_dir]
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
