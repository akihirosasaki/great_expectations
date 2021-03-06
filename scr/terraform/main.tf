resource "google_bigquery_dataset" "bigquery_dataset" {
  dataset_id    = "asasaki_data_infra_dataset"
  friendly_name = "asasaki_data_infra_dataset"
  location      = "us-central1"
}

resource "google_storage_bucket" "cloud_storage_bucket" {
  name = "sasakky_gcs_bucket"
  location      = "us-central1"
  force_destroy = true
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}

 /* Cloud Composerで動かす場合 */

# resource "google_composer_environment" "composer" {
#   name   = "composer-env"
#   region = "us-central1"
#   config {

#     software_config {
#       image_version = "composer-2.0.0-preview.3-airflow-2.1.2"
#     }

#     workloads_config {
#       scheduler {
#         cpu        = 0.5
#         memory_gb  = 1.875
#         storage_gb = 1
#         count      = 1
#       }
#       web_server {
#         cpu        = 0.5
#         memory_gb  = 1.875
#         storage_gb = 1
#       }
#       worker {
#         cpu = 0.5
#         memory_gb  = 1.875
#         storage_gb = 1
#         min_count  = 1
#         max_count  = 3
#       }


#     }
#     environment_size = "ENVIRONMENT_SIZE_SMALL"

#     node_config {
#       network    = google_compute_network.network.id
#       subnetwork = google_compute_subnetwork.subnet.id
#       service_account = ""
#     }
#   }
# }

# resource "google_compute_network" "network" {
#   name                    = "composer-network3"
#   auto_create_subnetworks = false
# }

# resource "google_compute_subnetwork" "subnet" {
#   name          = "composer-subnetwork"
#   ip_cidr_range = "10.2.0.0/16"
#   region        = "us-central1"
#   network       = google_compute_network.network.id
# }
