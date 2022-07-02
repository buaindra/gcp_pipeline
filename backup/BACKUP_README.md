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
4. Clean the infra
    ```shell
   terraform destroy 
   ```
   
