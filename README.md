# GCP Pipeline Workshop (*End To End Process*)

## Problem Statement:
> Currently cloud is only the solution for futuristic application, which can handle bigdata for both processing and storing.
> 
> There are lots of vendors and clients available who wants to migrate their application/data migration to the google cloud environment.
> 
> They expect some POCs/Workshops with the cloud developer to get confident to migrate their existing application/data to google cloud. 
> 
> This engagement process sometimes very time taking to understand their existing business approach and replicate same in cloud environment. 
> Also all best practices approach not work with their existing data stucture or application behaviour. 
> 
> So, we need some end to end pipeline in cloud which can create confidence to the customers to adopt cloud technology easily. Later they can customize 
> these code as per their requirements.
>

## Solution Approach:
> Here we are creating end to end pipeline in google cloud which will cover all types of gcp services and 
> apis.
>
> We have used below mentioned google apis with implementation of google best practices.
> 


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
1. (*Optional*) Install PyCharm IDE and create new project
   1. from PyCharm connect to git (git -> github -> share project on github)

2. (*Required*) Create virtual env inside pycharm project or local machine.
   

4. 


### How to set-up the infrustructure framework:
1. Create new Google Cloud Project:
   > Once you have completed the activity with this application, you can delete the project 
   > to save the unnecessary future cost
   >
   1. Make sure your account has project editor/owner role to get un-interupted execution.
   2. project should have linked with active billing account
   3. 
   

2. Clone the code from GIT Repo to cloudshell or VM Instances.
   ```shell
   mkdir working
   cd working
   git clone https://github.com/buaindra/gcp_pipeline.git
   git pull   *(repeated commands)*
   ```
3. Open terraform.tfvars and modify the changable parameter
   ```shell
   cd ~/working/gcp_pipeline/main/terraform   *(repeated commands)*
   vim terraform.tfvars  *(!wq)
   ```

3. Execute the terraform script from cloudshell as below:
   ```shell
   terraform init   *(repeated commands)*
   terraform plan   *(repeated commands)*
   terraform apply  *(repeated commands)*
   ```

4. For Email/ Message trigger, subscribe SendGrid API
   1. Ref:
      1. https://cloud.google.com/composer/docs/composer-2/configure-email
   2. Go to Google CLoud MarketPlace, Choose free plan, which is sufficient for our use-case.
   3. Click on "Manage On Provider"
      1. save your own details
      2. create sender (single sender creation with sender verification - who will send the email)
      3. verify your email as sender, and view the same inside Sendgrid UI -> Settings -> Sender Verification
      4. Create API Key
         1. go to settings -> API Key or Email API -> Integration Guide



### Clear your environment to save the cost
1. un-subsribe from sendgrid service
2. then, best thing is to delete the project to save cost.


### How to avoid known exceptions/errors:
1. terraform execution
   1. If terraform scripts are failing due to service not enabled, again call "terraform apply".
   
   