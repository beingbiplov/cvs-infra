terraform {
  backend "s3" {
    bucket  = "cert-verification-tf-state"
    key     = "phase1/s3/terraform.tfstate"
    region  = "eu-west-1"
    encrypt = true
  }
}
