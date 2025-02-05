provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "primary" {
  name               = var.cluster_name
  location           = var.region
  initial_node_count = var.node_count

  node_config {
    machine_type = var.node_machine_type
  }

  # Habilitar alias IP
  ip_allocation_policy {
    use_ip_aliases = true
  }
}

resource "google_container_node_pool" "primary_nodes" {
  cluster    = google_container_cluster.primary.name
  location   = var.region
  node_count = var.node_count

  node_config {
    machine_type = var.node_machine_type
  }
}

output "cluster_name" {
  value = google_container_cluster.primary.name
}
