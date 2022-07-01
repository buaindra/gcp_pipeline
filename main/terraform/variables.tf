variable "project_id" {
  type = string
}
variable "project_number" {
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
     "servicenetworking.googleapis.com",
#    "serviceusage.googleapis.com",
     "compute.googleapis.com",  # compute instance
     "sql-component.googleapis.com",  # cloud sql instance
     "storage.googleapis.com",
     "bigquery.googleapis.com",
     "bigquerystorage.googleapis.com",
     "composer.googleapis.com",  # cloud composer
     "secretmanager.googleapis.com"  # secret manager to store apikey for sendgrid, sql password
  ]
}

# cloudsql variables
variable "cloudsql_database_version" {
  type = string
}
variable "cloudsql_machine_type" {
  type = string
}
variable "cloudsql_user" {
  type = string
}
variable "cloudsql_pswd" {
  type = string
}

# cloud composer
variable "composer_name" {
  type = string
}
variable "composer_image_version" {
  type = string
}
