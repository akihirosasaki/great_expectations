provider "google" {
  project     = var.gcp_project_id
  region      = "us-central1"
  credentials = "${file("${var.GOOGLE_APPLICATION_CREDENTIALS}")}"
}