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
-   Run `terraform apply` to deploy google cloud resources in your gcp project.
    The command will prompt you to provide values for different input variables
    like `project_name` that will be used to deploy the resources.
-   You can also run `terraform plan` to validate resource declarations,
    identify any syntax errors, version mismatch etc.
