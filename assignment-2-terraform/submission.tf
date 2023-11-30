terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}
provider "google" {
  project = "terra-project-001"
  region  = "us-central1"
  zone    = "us-central1-c"
}
resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}
variable "vm_name_input" {
  type    = string
  default = "a-new-vm"
}
resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name_input
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }
  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}
resource "google_compute_firewall" "allow-ssh" {
  project = "terra-project-001"
  name    = "fw-allow-ssh"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports    = ["22", "80", "8080", "1000-2000"]
  }
  source_ranges = ["0.0.0.0/0"]
}
output "vm_name" {
  value = google_compute_instance.vm_instance.name
}
output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip
}
