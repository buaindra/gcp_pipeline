# GCP Pipeline Creation (*End To End Process*)

## Problem Statement:


## Solution Approach:

### PyCharm Git
1. git -> github -> share project on github

### Google Services/APIs covered:
1. Cloud IAM
1. Cloud Pub-Sub
2. Cloud Function (Python)
3. Cloud logging, Monitoring(alerting)
4. Cloud Dataproc (Pyspark)
5. Cloud Dataflow (Python, Beam)
6. Cloud SQL (Postgres)  
6. Cloud Bigquery
7. cloud GCS Bucket
7. Cloud Composer
8. Cloud Datastudio

### Other Services/tools/APIs:
1. Python Programming Language (Pycharm Editor)
2. SQL Scripting
3. Bash/Shell Scripting
4. Terraform Scripting

### Pre-Requisite:
1. Install below python packages into virtual env
    ```shell
    pip install 
    ```
   
### How to set-up the infrustructure framework:
1. Create new Google Cloud Project:
   1. Make sure your account has project editor/owner role to get un-interupted execution.

2. Clone the code from GIT Repo to cloudshell or VM Instances.
   ```shell
   mkdir working
   cd working
   git clone https://github.com/buaindra/gcp_pipeline.git
   
   ```

3. Execute the terraform script from cloudshell as below:
   ```shell
   cd working/gcp_pipeline/main/terraform
   terraform init
   terraform plan
   terraform apply
   ```
   
3. First create Service Account in Google IAM
   1. Ref:
      1.
   
3. 