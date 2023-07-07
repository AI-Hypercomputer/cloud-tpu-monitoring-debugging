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

data "google_project" "project" {
  project_id = var.project_name
}

// Add a dependency on log_metrics module to deploy log-based metrics before deploying logging dashboard
module "log_metrics" {
  source       = "./log_metrics"
  project_name = var.project_name
}

locals {
  dashboard_json = templatefile("${path.module}/dashboard_json/main.json",
    {
      TILE_1 = templatefile("${path.module}/dashboard_json/stack-trace-counter-metric.json",
        {
          METRIC_NAME = module.log_metrics.stack_trace_counter_metric_id
      }),
      TILE_2 = templatefile("${path.module}/dashboard_json/stack-trace-log-panel.json",
        {
          PROJECT_NUMBER = data.google_project.project.number
      })
  })
}

resource "google_monitoring_dashboard" "logging_dashboard" {
  project        = var.project_name
  dashboard_json = local.dashboard_json
  depends_on     = [module.log_metrics.stack_trace_counter_metric]
}
