provider "google" {
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