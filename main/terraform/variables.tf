variable "project_id" {
  type = string
}
variable "region" {
  type = string
}
variable "zone" {
  type = string
}
variable "deletion_protection" {
  type = string
}

# IAM Variables
variable "sa_id" {
  type = string
  default = "sa-gcp-pipeline"
}

# google services/apis variables
variable "gcp_service_list" {
  description ="The list of apis necessary for the project"
  type = list(string)
  default = [
     "cloudresourcemanager.googleapis.com",
     "iam.googleapis.com",
#    "serviceusage.googleapis.com",
     "compute.googleapis.com",  # compute instance
     "sql-component.googleapis.com",  # cloud sql instance
     "storage.googleapis.com",
     "bigquery.googleapis.com",
     "bigquerystorage.googleapis.com",
     "composer.googleapis.com"  # cloud composer
  ]
}

# cloudsql variables
variable "cloudsql_name" {
  type = string
}

variable "cloudsql_database_version" {
  type = string
}

variable "cloudsql_machine_type" {
  type = string
}