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

resource "google_project_iam_binding" "sa_role_4" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${google_service_account.service_account.email}"
  ]
  depends_on = [google_service_account.service_account]
}


# create cloudsql with postgres --start--

resource "google_compute_network" "private_network" {
  name = "private-network"
  # auto_create_subnetworks = false
  depends_on = [google_service_account.service_account]
}

#resource "google_compute_subnetwork" "test" {
#  name          = "composer-test-subnetwork"
#  ip_cidr_range = "10.2.0.0/16"
#  region        = "us-central1"
#  network       = google_compute_network.test.id
#}

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

resource "google_sql_user" "users" {
  name     = var.cloudsql_user
  instance = google_sql_database_instance.instance.name
  password = var.cloudsql_pswd
  depends_on = [google_sql_database_instance.instance]
}

# create cloudsql with postgres --end--

#create cloud composer --start--
resource "google_project_iam_member" "composer-service-agent" {
  project  = var.project_id
  role     = "roles/composer.ServiceAgentV2Ext"   # this is require for composer version 2
  member   = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "composer-worker" {
  project = var.project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_composer_environment" "composer_env" {
  name   = var.composer_name
  region = var.region
  config {
    software_config {
      image_version = var.composer_image_version
    }

    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
      }
      worker {
        cpu = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        min_count  = 1
        max_count  = 3
      }


    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      network    = google_compute_network.private_network.id
      #subnetwork = google_compute_subnetwork.test.id
      service_account = google_service_account.service_account.name
    }
  }
  depends_on = [google_project_iam_member.composer-service-agent,
    google_project_iam_member.composer-worker]
}

resource "google_composer_environment" "composer_env-update" {
  name   = var.composer_name
  region = var.region

  config {
    software_config {
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "True"
      }

      # "[Extra]==Version"
      pypi_packages = {
          numpy = ""
          scipy = "==1.1.0"
          cloud-sql-python-connector = "[pg8000]"
          SQLAlchemy = ""
          google-cloud-logging = ""
          google-cloud-storage = ""
          google-cloud-bigquery = ""
          apache-airflow-providers-sendgrid = ""
      }

      env_variables = {
        FOO = "bar"
      }
    }
  }
  depends_on = [google_composer_environment.composer_env]
}

# cloud pub-sub