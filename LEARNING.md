## Learning

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
    2. 
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











