provider "google" {
  project = var.project_id
  region = var.region
  zone   = var.zone
}

# enable google cloud services
resource "google_project_service" "gcp_services" {
  for_each = toset(var.gcp_service_list)
  project = var.project_id
  service = each.key

  provisioner "local-exec" {
    command = "sleep 5"
  }
}

#create service account
resource "google_service_account" "service_account" {
  account_id   = var.sa_id
  display_name = var.sa_id
  description = "created this sa for gcp pipeline project"
  project = var.project_id

  # as in same config we are applying roles to the same service account
  provisioner "local-exec" {
    command = "sleep 5"
  }
  depends_on = [google_project_service.gcp_services]
}

# Provide IAM role binding withthe newly created service account
resource "google_project_iam_binding" "sa_role_1" {
  project = var.project_id
  role    = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.service_account.email}"
  ]
  depends_on = [google_service_account.service_account]
}

resource "google_project_iam_binding" "sa_role_2" {
  project = var.project_id
  role    = "roles/serviceusage.serviceUsageAdmin"
  members = [
    "serviceAccount:${google_service_account.service_account.email}"
  ]
  depends_on = [google_service_account.service_account]
}

resource "google_project_iam_binding" "sa_role_3" {
  project = var.project_id
  role    = "roles/cloudsql.admin"
  members = [
    "serviceAccount:${google_service_account.service_account.email}"
  ]
  depends_on = [google_service_account.service_account]
}


# create cloudsql with postgres
resource "google_compute_network" "private_network" {
  name = "private-network"
  depends_on = [google_service_account.service_account]
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
  depends_on = [google_compute_network.private_network]
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
  depends_on = [google_compute_global_address.private_ip_address]
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "instance" {
  name             = "private-instance-${random_id.db_name_suffix.hex}"
  region           = var.region
  database_version = var.cloudsql_database_version
  deletion_protection = var.deletion_protection

  depends_on = [google_service_account.service_account, google_service_networking_connection.private_vpc_connection]

  settings {
    tier = var.cloudsql_machine_type
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.private_network.id
    }
  }
}