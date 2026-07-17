terraform {
  required_version = ">= 1.0.0"
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# 1. Compartment setup
resource "oci_identity_compartment" "hospitality_compartment" {
  compartment_id = var.tenancy_ocid
  description    = "Hospitality AI Platform Infrastructure Compartment"
  name           = "hospitality-ai"
}

# 2. Virtual Cloud Network (VCN)
resource "oci_core_vcn" "hospitality_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  display_name   = "hospitality-vcn"
  dns_label      = "hospitality"
}

# Gateways
resource "oci_core_internet_gateway" "ig" {
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  display_name   = "internet-gateway"
  vcn_id         = oci_core_vcn.hospitality_vcn.id
}

resource "oci_core_nat_gateway" "nat" {
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  display_name   = "nat-gateway"
  vcn_id         = oci_core_vcn.hospitality_vcn.id
}

# Subnets
resource "oci_core_subnet" "public_subnet" {
  cidr_block     = "10.0.1.0/24"
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  vcn_id         = oci_core_vcn.hospitality_vcn.id
  display_name   = "public-subnet"
  dns_label      = "public"
  route_table_id = oci_core_vcn.hospitality_vcn.default_route_table_id
}

resource "oci_core_subnet" "private_worker_subnet" {
  cidr_block                 = "10.0.2.0/24"
  compartment_id             = oci_identity_compartment.hospitality_compartment.id
  vcn_id                     = oci_core_vcn.hospitality_vcn.id
  display_name               = "private-worker-subnet"
  dns_label                  = "workers"
  prohibit_public_ip_on_vnic = true
}

# 3. Container Engine for Kubernetes (OKE)
resource "oci_containerengine_cluster" "oke_cluster" {
  compartment_id     = oci_identity_compartment.hospitality_compartment.id
  kubernetes_version = "v1.30.1"
  name               = "hospitality-oke-cluster"
  vcn_id             = oci_core_vcn.hospitality_vcn.id

  options {
    service_lb_subnet_ids = [oci_core_subnet.public_subnet.id]
  }
}

# 4. Object Storage Buckets
resource "oci_objectstorage_bucket" "knowledge_bucket" {
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  name           = "hospitality-knowledge-bucket"
  namespace      = var.storage_namespace
  access_type    = "NoPublicAccess"
}

resource "oci_objectstorage_bucket" "mlflow_bucket" {
  compartment_id = oci_identity_compartment.hospitality_compartment.id
  name           = "hospitality-mlflow-bucket"
  namespace      = var.storage_namespace
  access_type    = "NoPublicAccess"
}
