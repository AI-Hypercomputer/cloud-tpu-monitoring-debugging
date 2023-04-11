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

# TpuMonitoringDebugging

## Overview

Terraform is an open-source tool to set up and manage google cloud
infrastructure based on configuration files. This repository will help the
customers to deploy various google cloud resources via script, without any
manual effort.

## Getting Started

-   Install Terraform on desktop:
    https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli
-   In the module directory containing `main.tf`, run `terraform init` to
    initialize google cloud Terraform provider version. This command will add
    the necessary plugins and build the `.terraform` directory.
-   If there is an update to terraform google cloud provider version, run
    `terraform init --upgrade` for the update to take place.
-   Run `terraform apply -var outlier_count=<count of outliers for monitoring
    dashboard> -var project_name="<name of gcp project>"` to deploy google cloud
    resources in your gcp project. If `outlier_count` variable is missing from
    the command, terraform will take the default value (10 in this case).
-   You can also run `terraform apply` to deploy the resources that will prompt
    you to provide values for different input variables with no default values
    like `project_name` in this case. The command will use the default values set for other variables.
-   You can also run `terraform plan` to validate resource declarations,
    identify any syntax errors, version mismatch etc.
