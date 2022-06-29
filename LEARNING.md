## Learning

### Cloud IAM:
1. Roles
   1. Ref:
      1. https://cloud.google.com/iam/docs/understanding-roles
   

### Cloud Composer:
1. Airflow concepts:
    1. Ref:
        1. https://airflow.apache.org/docs/apache-airflow/1.10.2/concepts.html
        2. https://airflow.apache.org/docs/apache-airflow/2.3.2/tutorial.html

2. Airflow Contrib vs Provider Module:
    1. Always use Provider module and contrib is depricated.
    2. Ref: https://stackoverflow.com/questions/70243008/diff-between-airflow-providers-and-airflow-contrib

   
### Terraform:
1. Terraform Learning:
   1. Ref:
       1. https://www.youtube.com/watch?v=jJX6S5JAGpI&list=PL7iMyoQPMtAOz187ezONf7pL8oGZRobYl
1. Terraform module concept
    1. Ref: 
       1. https://blog.gruntwork.io/how-to-create-reusable-infrastructure-with-terraform-modules-25526d65f73d
   
2. Sample Terraform Code Snippet:
   ```shell
   terraform init
   terraform plan
   terraform apply
   terraform destroy
   ```
   
3. terraform init
   1. To initialize a working directory that contains a Terraform configuration. After initialization, you will be able to perform other commands, like terraform plan and terraform apply

4. **variables.tf vs terraform.tfvars**:
   1. Ref:
      1. https://www.youtube.com/watch?v=oB7l8GOpVaY
   1. A **variables.tf** file is used to define the variables type and optionally set a default value.
   2. A **terraform.tfvars** file is used to set the actual values of the variables.
   
5. terraform with postgres cloud sql:
   1. Ref: 
      1. https://github.com/gruntwork-io/terraform-google-sql/tree/master/examples/postgres-private-ip
      2. https://medium.com/swlh/how-to-deploy-a-cloud-sql-db-with-a-private-ip-only-using-terraform-e184b08eca64
      3. https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance#deletion_protection
   
6. terraform with cloud composer:
   1. Ref:
      1. https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/composer_environment#argument-reference---cloud-composer-2
   


### Bash Command
```shell
cd ~  # change directory to default home 
ls -lart
```






