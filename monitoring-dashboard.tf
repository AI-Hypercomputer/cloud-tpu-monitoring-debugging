/*
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
*/

locals {
  dashboard_json = templatefile("${path.module}/monitoring_dashboard_json/main.json",
        {
          TILE_1 = file("${path.module}/monitoring_dashboard_json/cpu-utilization.json"),
          TILE_2 = file("${path.module}/monitoring_dashboard_json/tensorcore-idle-duration.json"),
          TILE_3 = file("${path.module}/monitoring_dashboard_json/memory-usage.json"),
          TILE_4 = file("${path.module}/monitoring_dashboard_json/network-bytes.json")
        })
}

resource "google_monitoring_dashboard" "monitoring_dashboard" {
 project     = var.project_name
 dashboard_json = local.dashboard_json
}
