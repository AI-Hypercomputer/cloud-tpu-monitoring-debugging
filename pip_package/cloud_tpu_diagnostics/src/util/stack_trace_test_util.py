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

"""Script to raise different signals to test dumping of stack trace."""

import argparse
import signal

from cloud_tpu_diagnostics import diagnostic


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--signal', help='name of signal to raise')
  parser.add_argument('--trace_dir', help='path of trace directory')
  args = parser.parse_args()

  with diagnostic.diagnose():
    if args.signal == 'SIGSEGV':
      signal.raise_signal(signal.SIGSEGV)

    if args.signal == 'SIGABRT':
      signal.raise_signal(signal.SIGABRT)

    if args.signal == 'SIGFPE':
      signal.raise_signal(signal.SIGFPE)

    if args.signal == 'SIGILL':
      signal.raise_signal(signal.SIGILL)

    if args.signal == 'SIGBUS':
      signal.raise_signal(signal.SIGBUS)

    if args.signal == 'SIGUSR1':
      signal.raise_signal(signal.SIGUSR1)
