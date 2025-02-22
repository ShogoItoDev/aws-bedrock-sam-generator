provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS region to create resources"
  default     = "us-east-1"
}

variable "system_identifier" {
  description = "A unique identifier for the system"
  default     = "4405110"
}