module "certificate_bucket" {
  source       = "./modules/s3"
  project_name = var.project_name
  environment  = var.environment
}
