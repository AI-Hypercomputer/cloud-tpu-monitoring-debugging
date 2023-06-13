<!--
 Copyright 2023 Google LLC
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
      https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->
# Cloud TPU Diagnostics

This is a comprehensive library to monitor, debug and profile the jobs running on Cloud TPU.
To learn about Cloud TPU, refer to the [full documentation](https://cloud.google.com/tpu/docs/intro-to-tpu).

## Features
### 1. Debugging
#### 1.1 Collect Stack Traces
This module will dump the python traces when a fault such as Segmentation fault, Floating-point exception, Illegal operation exception occurs in the program. Additionally, it will also periodically collect stack traces to help debug when a program running on Cloud TPU is stuck or hung somewhere.

## Installation
To install the package, run the following command on TPU VM:

```
pip install cloud-tpu-diagnostics
```

## Usage
To use this package, first import the module:

```
from cloud_tpu_diagnostics import diagnostic
from cloud_tpu_diagnostics.configuration import debug_configuration
from cloud_tpu_diagnostics.configuration import diagnostic_configuration
from cloud_tpu_diagnostics.configuration import stack_trace_configuration
```

Then, create configuration object for stack traces. The module will only collect stack traces when `collect_stack_trace` parameter is set to `True`. There are following scenarios supported currently:

##### Scenario 1: Do not collect stack traces on faults

```
stack_trace_config = stack_trace_configuration.StackTraceConfig(
                      collect_stack_trace=False)
```
This configuration will prevent you from collecting stack traces in the event of a fault or process hang.

##### Scenario 2: Collect stack traces on faults and display on console

```
stack_trace_config = stack_trace_configuration.StackTraceConfig(
                      collect_stack_trace=True,
                      stack_trace_to_cloud=False)
```
If there is a fault or process hang, this configuration will show the stack traces on the console (stderr).

##### Scenario 3: Collect stack traces on faults and upload on cloud

```
stack_trace_config = stack_trace_configuration.StackTraceConfig(
                      collect_stack_trace=True,
                      stack_trace_to_cloud=True)
```
This configuration will temporary collect stack traces inside `/tmp/debugging` directory on TPU host if there is a fault or process hang. Additionally, the traces collected in TPU host memory will be uploaded to Google Cloud Logging, which will make it easier to troubleshoot and fix the problems. You can view the traces in [Logs Explorer](https://cloud.google.com/logging/docs/view/logs-explorer-interface) using the following query:

```
logName="projects/<project_name>/logs/tpu.googleapis.com%2Fruntime_monitor"
jsonPayload.verb="stacktraceanalyzer"
```

By default, stack traces will be collected every 10 minutes. In order to change the duration between two stack trace collection events, add the following configuration:

```
stack_trace_config = stack_trace_configuration.StackTraceConfig(
                      collect_stack_trace=True,
                      stack_trace_to_cloud=True,
                      stack_trace_interval_seconds=300)
```
This configuration will collect the stack traces on cloud after every 5 minutes.

Then, create configuration object for debug.

```
debug_config = debug_configuration.DebugConfig(
                stack_trace_config=stack_trace_config)
```

Then, create configuration object for diagnostic.

```
diagnostic_config = diagnostic_configuration.DiagnosticConfig(
                      debug_config=debug_config)
```

Finally, call the `diagnose()` method using `with` and wrap the statements inside the context manager for which you want to collect the stack traces.

```
with diagnostic.diagnose(diagnostic_config):
    run_job(...)
```