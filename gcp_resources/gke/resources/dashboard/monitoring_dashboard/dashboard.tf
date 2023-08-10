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
  outlier_count = var.monitoring_dashboard_config.outlier_count == null ? 10 : var.monitoring_dashboard_config.outlier_count
  dashboard_json = templatefile("${path.module}/dashboard_json/main.json",
    {
      TILE_1 = templatefile("${path.module}/dashboard_json/cpu-utilization.json",
        {
          OUTLIER_COUNT = local.outlier_count
      }),
      TILE_2 = templatefile("${path.module}/dashboard_json/memory-usage.json",
        {
          OUTLIER_COUNT = local.outlier_count
      }),
      TILE_3 = templatefile("${path.module}/dashboard_json/accelerator-memory-used.json",
        {
          OUTLIER_COUNT = local.outlier_count
      }),
      TILE_4 = templatefile("${path.module}/dashboard_json/duty-cycle.json",
        {
          OUTLIER_COUNT = local.outlier_count
      }),
      TILE_5 = templatefile("${path.module}/dashboard_json/network-bytes.json",
        {
          OUTLIER_COUNT = local.outlier_count
      })
  })
}

resource "google_monitoring_dashboard" "monitoring_dashboard" {
  project        = var.project_name
  dashboard_json = local.dashboard_json
}
