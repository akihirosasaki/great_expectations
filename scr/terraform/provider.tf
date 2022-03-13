provider "google" {
  project     = var.gcp_project_id
  region      = "asia-northeast1"
  # credentials = "${file("${var.GOOGLE_APPLICATION_CREDENTIALS}")}"
  credentials = "${file("../../../secrets/gcp_secret_key_test_asasaki_data_owner.json")}"
}