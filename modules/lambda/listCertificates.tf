data "archive_file" "list_certificates_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src/listCertificates"
  output_path = "${path.module}/list_certificates_lambda.zip"
}

resource "aws_lambda_function" "list_certificates" {
  function_name = "${var.project_name}-${var.environment}-list-certificates"
  runtime       = "python3.11"
  handler       = "list_handler.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  timeout     = 15
  memory_size = 256

  filename         = data.archive_file.list_certificates_lambda_zip.output_path
  source_code_hash = data.archive_file.list_certificates_lambda_zip.output_base64sha256

  environment {
    variables = {
      CERTIFICATE_TABLE = var.dynamodb_table_name
      USER_INDEX_NAME   = "userId-createdAt-index"
    }
  }
}
