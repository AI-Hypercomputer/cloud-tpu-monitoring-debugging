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
  name        = "stack_trace_counter_gke"
  project     = var.project_name
  description = "Counts the number of stack trace log entries within a specific period."
  filter      = "resource.type=\"k8s_container\" AND resource.labels.container_name=~\"[a-z-0-9]*stacktrace[a-z-0-9]*\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    labels {
      key        = "location"
      value_type = "STRING"
    }
    labels {
      key        = "cluster"
      value_type = "STRING"
    }
    labels {
      key        = "pod"
      value_type = "STRING"
    }
    labels {
      key        = "job_name"
      value_type = "STRING"
    }
  }
  label_extractors = {
    "location" = "EXTRACT(resource.labels.location)",
    "cluster"  = "EXTRACT(resource.labels.cluster_name)",
    "pod"      = "EXTRACT(resource.labels.pod_name)",
    "job_name" = "EXTRACT(labels.k8s-pod/job-name)",
  }
}

output "stack_trace_counter_metric_id" {
  value = google_logging_metric.stack_trace_counter_metric.id
}
