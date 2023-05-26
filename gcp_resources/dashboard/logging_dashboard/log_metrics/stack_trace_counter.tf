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

// Metric that counts the number of stack trace entries that match a specified filter within a specific period
resource "google_logging_metric" "stack_trace_counter_metric" {
  name        = "stack_trace_counter"
  project     = var.project_name
  description = "Counts the number of stack trace log entries within a specific period."
  filter      = "resource.type=\"tpu_worker\" AND log_id(\"tpu.googleapis.com/runtime_monitor\") AND jsonPayload.verb=\"stacktraceanalyzer\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    labels {
      key        = "zone"
      value_type = "STRING"
    }
    labels {
      key        = "node_id"
      value_type = "STRING"
    }
    labels {
      key        = "worker_id"
      value_type = "STRING"
    }
  }
  label_extractors = {
    "zone"      = "EXTRACT(resource.labels.zone)",
    "node_id"   = "EXTRACT(resource.labels.node_id)",
    "worker_id" = "EXTRACT(resource.labels.worker_id)",
  }
}

output "stack_trace_counter_metric_id" {
  value = google_logging_metric.stack_trace_counter_metric.id
}
