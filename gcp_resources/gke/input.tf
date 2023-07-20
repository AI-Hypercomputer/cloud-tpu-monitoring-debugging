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

variable "project_name" {
  type        = string
  description = "Name of gcp project"
}

variable "monitoring_dashboard_config" {
  type = object({
    outlier_count : optional(number)
  })
  description = <<EOF
  Configuration for monitoring dashboard:
  {
    "outlier_count": "number of outliers to show on dashboard, default to 10 if not set"
  }
  Enter {} to set default configuration for monitoring dashboard.
  EOF
}

// Valid inputs:
// 1. To create stack trace bucket for 30 retention days: {"bucket_name":"<log_bucket_name>"}
// 2. To create stack trace bucket for x retention days: {"bucket_name":"<log_bucket_name>", "retention_days":x}
// 3. To not create stack trace bucket: {}
variable "stack_trace_bucket_config" {
  type = object({
    bucket_name : optional(string)
    retention_days : optional(number)
  })
  validation {
    condition = (
      (var.stack_trace_bucket_config.bucket_name == null &&
      var.stack_trace_bucket_config.retention_days == null) ||
      (var.stack_trace_bucket_config.bucket_name != null)
    )
    error_message = "bucket_name is not defined for stack_trace_bucket_config."
  }
  description = <<EOF
  Configuration to create a log bucket to store stack traces:
  {
    "bucket_name": "name of log bucket to create",
    "retention_days": number of days to retain stack traces, default to 30 days if not set
  }
  Enter {} to not create separate log bucket for stack traces.
  EOF
}
