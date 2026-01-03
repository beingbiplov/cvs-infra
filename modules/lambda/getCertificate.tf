data "archive_file" "get_certificate_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src/getCertificate"
  output_path = "${path.module}/get_certificate_lambda.zip"
}


resource "aws_lambda_function" "get_certificate" {
  function_name = "${var.project_name}-${var.environment}-get-certificate"
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  timeout     = 10
  memory_size = 256

  filename         = data.archive_file.get_certificate_lambda_zip.output_path
  source_code_hash = data.archive_file.get_certificate_lambda_zip.output_base64sha256

  environment {
    variables = {
      CERTIFICATE_TABLE = var.dynamodb_table_name
    }
  }
}
