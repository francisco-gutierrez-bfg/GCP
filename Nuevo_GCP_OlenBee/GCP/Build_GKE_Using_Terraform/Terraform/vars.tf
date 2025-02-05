variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región donde se creará el clúster"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "Nombre del clúster"
  type        = string
}

variable "node_count" {
  description = "Número de nodos"
  type        = number
  default     = 3
}

variable "node_machine_type" {
  description = "Tipo de máquina para los nodos"
  type        = string
  default     = "e2-medium"
}
