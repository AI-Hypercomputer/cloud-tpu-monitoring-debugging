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

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.57.0"
    }
  }
}

module "monitoring_dashboard" {
  source        = "./resources/dashboard/monitoring_dashboard"
  project_name  = var.project_name
  monitoring_dashboard_config = var.monitoring_dashboard_config
}

module "logging_dashboard" {
  source       = "./resources/dashboard/logging_dashboard"
  project_name = var.project_name
}

module "log_storage" {
  source                    = "./resources/log_storage"
  project_name              = var.project_name
  stack_trace_bucket_config = var.stack_trace_bucket_config
}
