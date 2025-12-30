variable "project_name" {
  description = "Project name prefix"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket for certificates"
  type        = string
}

variable "bucket_arn" {
  description = "ARN of the S3 bucket for certificates"
  type        = string
}