module "certificate_bucket" {
  source       = "./modules/s3"
  project_name = var.project_name
  environment  = var.environment
}

module "certificates_table" {
  source = "./modules/dynamodb"

  project_name = var.project_name
  environment  = var.environment
}

module "certificate_lambda" {
  source = "./modules/lambda"

  project_name = var.project_name
  environment  = var.environment
  bucket_arn   = module.certificate_bucket.bucket_arn
  bucket_name  = module.certificate_bucket.bucket_name
  dynamodb_table_arn  = module.certificates_table.table_arn
  dynamodb_table_name = module.certificates_table.table_name
}

module "certificate_api" {
  source = "./modules/api-gateway"

  environment                = var.environment
  presign_lambda_invoke_arn  = module.certificate_lambda.invoke_arn
  presign_lambda_name        = module.certificate_lambda.lambda_function_name
  get_certificate_lambda_invoke_arn = module.certificate_lambda.get_certificate_lambda_invoke_arn
  get_certificate_lambda_function_name       = module.certificate_lambda.get_certificate_lambda_function_name
}

module "cognito" {
  source = "./modules/cognito"

  project_name = var.project_name
  environment  = var.environment
}
