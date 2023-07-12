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

### Configure Terraform to store state in Cloud Storage

By default, Terraform stores [state](https://www.terraform.io/docs/state/) locally in a file named `terraform.tfstate`. This default configuration can make Terraform usage difficult for teams, especially when many users run Terraform at the same time and each machine has its own understanding of the current infrastructure. To help avoid such issues, this section configures a remote state that points to Google Cloud Storage (GCS) bucket.

1. In Cloud Shell, create the GCS bucket:

        gsutil mb gs://${GCS_BUCKET_NAME}

2. Enable [Object Versioning](https://cloud.google.com/storage/docs/object-versioning) to keep the history of your deployments. Enabling Object Versioning increases [storage costs](https://cloud.google.com/storage/pricing), which you can mitigate by configuring
[Object Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle) to delete old state versions.

        gsutil versioning set on gs://${GCS_BUCKET_NAME}

3. Enter the name of GCS bucket created above when you run `terraform init` to initialize Terraform.

        Initializing the backend...
        bucket
          The name of the Google Cloud Storage bucket

          Enter a value: <GCS_BUCKET_NAME>

## Deploy GCP Resources
There are following resources managed in this directory:

1. **Monitoring Dashboard**: This is an outlier dashboard that displays statistics and outlier mode for TPU metrics.
2. **Debugging Dashboard**: This dashboard displays the stack traces collected in Cloud Logging for the process running on TPU VMs.
3. **Logging Storage**: This is an user-defined log bucket to store stack traces. Creating a new log storage is completely optional. If you choose not to create a separate log bucket, the stack traces will be collected in [_Default log bucket](https://cloud.google.com/logging/docs/routing/overview#default-bucket).

### Deploy Resources for Workloads on GCE

Run `terraform init && terraform apply` inside `gcp_resources/gce` directory to deploy all the resources mentioned above for TPU workloads running on GCE. You will be prompted to provide values for some input variables. After confirming the action, all the resources will get automatically deployed in your gcp project.

### Deploy Resources for Workloads on GKE

Run `terraform init && terraform apply` inside `gcp_resources/gke` directory to deploy all the resources mentioned above for TPU workloads running on GKE. You will be prompted to provide values for some input variables. After confirming the action, all the resources will get automatically deployed in your gcp project.

Note: Please check the below guide for GCE/GKE specific prerequisites.

Follow the below guide to deploy the resources individually:
### Monitoring Dashboard
#### GCE
Run `terraform init && terraform apply` inside `gcp_resources/gce/resources/dashboard/monitoring_dashboard/` to deploy only monitoring dashboard for GCE in your gcp project.

#### GKE
Run `terraform init && terraform apply` inside `gcp_resources/gke/resources/dashboard/monitoring_dashboard/` to deploy only monitoring dashboard for GKE in your gcp project.

### Debugging Dashboard
#### GCE
Run `terraform init && terraform apply` inside `gcp_resources/gce/resources/dashboard/logging_dashboard/` to deploy only debugging dashboard for GCE in your gcp project.

#### GKE
Run `terraform init && terraform apply` inside `gcp_resources/gke/resources/dashboard/logging_dashboard/` to deploy only debugging dashboard for GKE in your gcp project.

Users need to add a sidecar container to their TPU workload running on GKE to view traces in the debugging dashboard. The sidecar container must be named in a specific way, matching the regex `[a-z-0-9]*stacktrace[a-z-0-9]*`. Here is an example of the sidecar container that should be added:

```
containers:
- name: stacktrace-log-collector
  image: busybox:1.28
  resources:
    limits:
      cpu: 100m
      memory: 200Mi
  args: [/bin/sh, -c, "while [ ! -d /tmp/debugging ]; do sleep 60; done; while [ ! -e /tmp/debugging/* ]; do sleep 60; done; tail -n+1 -f /tmp/debugging/*"]
  volumeMounts:
  - name: tpu-debug-logs
    readOnly: true
    mountPath: /tmp/debugging
- name: <main_container>
.....
.....
volumes:
- name: tpu-debug-logs
```

### Log Storage
#### GCE
Run `terraform init && terraform apply` inside `gcp_resources/gce/resources/log_storage/` to deploy a separate log bucket to store stack traces for GCE. You will be prompted to provide name of your gcp project and also the bucket configuration. You can also set the retention period for the bucket.