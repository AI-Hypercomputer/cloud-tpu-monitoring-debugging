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

locals {
  stack_trace_filter         = "projects/${var.project_name}/logs/tpu.googleapis.com%2Fruntime_monitor AND jsonPayload.verb=stacktraceanalyzer"
  stack_trace_bucket_counter = var.stack_trace_bucket_config.bucket_prefix == null ? 0 : 1
}

resource "google_logging_project_bucket_config" "log_bucket" {
  count    = local.stack_trace_bucket_counter
  project  = var.project_name
  location = "global"
  // default retention period is 30 days
  retention_days = var.stack_trace_bucket_config.retention_days == null ? 30 : var.stack_trace_bucket_config.retention_days
  bucket_id      = "${var.stack_trace_bucket_config.bucket_prefix}_log_bucket"
}

resource "google_logging_project_sink" "log_sink" {
  count       = local.stack_trace_bucket_counter
  project     = var.project_name
  name        = "${var.stack_trace_bucket_config.bucket_prefix}_log_sink"
  destination = "logging.googleapis.com/projects/${var.project_name}/locations/global/buckets/${google_logging_project_bucket_config.log_bucket[count.index].bucket_id}"
  filter      = local.stack_trace_filter
}
