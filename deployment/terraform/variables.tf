variable "tenancy_ocid" {
  type        = string
  description = "OCI Tenancy OCID"
}

variable "user_ocid" {
  type        = string
  description = "OCI User OCID"
}

variable "fingerprint" {
  type        = string
  description = "OCI API Key Fingerprint"
}

variable "private_key_path" {
  type        = string
  description = "Path to OCI private key file"
}

variable "region" {
  type        = string
  default     = "us-ashburn-1"
  description = "OCI Region"
}

variable "storage_namespace" {
  type        = string
  description = "OCI Storage Object Namespace"
}
