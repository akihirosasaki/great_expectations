resource "google_bigquery_dataset" "bigquery_dataset" {
  dataset_id    = "asasaki_data_infra_dataset"
  friendly_name = "asasaki_data_infra_dataset"
  location      = "us-central1"
}
