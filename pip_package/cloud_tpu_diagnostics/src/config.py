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


def bool_env(varname, default):
  """Read an environment variable and interpret it as a boolean.

  True values are (case insensitive): 'y', 'yes', 't', 'true', 'on', and '1'
  False values are 'n', 'no', 'f', 'false', 'off', and '0'.

  Args:
    varname: the name of the variable
    default: the default boolean value
  Raises: ValueError if the environment variable is anything else.

  Returns:
    Boolean value of the environment variable.
  """
  value = os.getenv(varname, str(default))
  value = value.lower()
  if value in ('y', 'yes', 't', 'true', 'on', '1'):
    return True
  elif value in ('n', 'no', 'f', 'false', 'off', '0'):
    return False
  else:
    raise ValueError(
        f'Invalid value {value} for environment variable {varname}'
    )


class Config:
  # Set True to dynamically add new attributes
  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self):
    self.values = {}

  def add_option(self, name, value):
    name = name.lower()
    if name in self.values:
      raise ValueError(f'Config option {name} already defined.')
    self.values[name] = value
    setattr(Config, name, value)

  def define_bool(self, name, default, **unused_args):
    """Set up config option for boolean.

    Sets config for boolean using environment variable or the default value.

    Args:
      name: string, name of the config option. It is converted to uppercase to
        define the corresponding shell environment variable.
      default: boolean, a default value for the option.
    """
    self.add_option(name, bool_env(name.upper(), default))

  def define_string(self, name, default, **unused_args):
    """Set up config option for string.

    Sets config for string using environment variable or the default value.

    Args:
      name: string, name of the config option. It is converted to uppercase to
        define the corresponding shell environment variable.
      default: string, a default value for the option.
    """
    self.add_option(name, os.getenv(name.upper(), str(default)))


config = Config()

config.define_bool(
    name='collect_stack_trace',
    default=False,
    help=(
        'Enable collection of stack trace in case fault occurs in the program. '
        'Default is False, which means stack trace will not be collected '
        'unless COLLECT_STACK_TRACE environment variable is set to True.'
    ),
)

config.define_string(
    name='stack_trace_dir',
    default='/tmp/',
    help=(
        'Directory to store stack trace when a fault occurs in the program. '
        'Default is /tmp/, which means stack trace will be collected inside '
        '/tmp/ directory unless STACK_TRACE_DIR environment variable is set.'
    ),
)
