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
# Cloud TPU Monitoring Debugging

## Overview

Cloud TPU Monitoring Debugging repository contains all the infrastructure and logic required to monitor and debug jobs running on Cloud TPU.

Terraform is used to deploy resources in google cloud project.
Terraform is an open-source tool to set up and manage google cloud
infrastructure based on configuration files. This repository will help the
customers to deploy various google cloud resources via script, without any
manual effort.

[cloud-tpu-diagnostics PyPI package]((https://pypi.org/project/cloud-tpu-diagnostics)) contains all the logic to monitor, debug and profile the jobs running on Cloud TPU.

## Getting Started with Terraform

-   Follow [this link](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli) to install Terraform on desktop.
-   Run `terraform init` to
    initialize google cloud Terraform provider version. This command will add
    the necessary plugins and build the `.terraform` directory.
-   If there is an update to terraform google cloud provider version, run
    `terraform init --upgrade` for the update to take place.
-   You can also run `terraform plan` to validate resource declarations,
    identify any syntax errors, version mismatch before deploying the resources.

## Deploy GCP Resources
There are following resources managed in this directory:

1. **Monitoring Dashboard**: This is an outlier dashboard that displays statistics and outlier mode for TPU metrics.
2. **Debugging Dashboard**: This dashboard displays the stack traces collected in Cloud Logging for the process running on TPU VMs.
3. **Logging Storage**: This is an user-defined log bucket to store stack traces. Creating a new log storage is completely optional. If you choose not to create a separate log bucket, the stack traces will be collected in [_Default log bucket](https://cloud.google.com/logging/docs/routing/overview#default-bucket).

Run `terraform apply -var outlier_count=<count of outliers for monitoring dashboard>` inside `gcp_resources/` directory to deploy all the resources mentioned above. You will be prompted to provide values for some input variables. If `outlier_count` variable is missing from the command, terraform will take the default value (10 in this case). After confirming the action, all the resources will get automatically deployed in your gcp project.

Follow the below guide to deploy the resources individually:
### Monitoring Dashboard
Run `terraform init && terraform apply -var outlier_count=<count of outliers for monitoring dashboard>` inside `gcp_resources/dashboard/monitoring_dashboard/` to deploy only outlier dashboard in your gcp project. If `outlier_count` variable is missing from the command, terraform will take the default value (10 in this case).

### Debugging Dashboard
Run `terraform init && terraform apply` inside `gcp_resources/dashboard/logging_dashboard/` to deploy only debugging dashboard in your gcp project.

### Log Storage
Run `terraform init && terraform apply` inside `gcp_resources/log_storage/` to deploy a separate log bucket to store stack traces. You will be prompted to provide name of your gcp project and also the bucket configuration. You can also set the retention period for the bucket.