data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src/presign"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "certificate_presign" {
  function_name = "${var.project_name}-${var.environment}-certificate-presign"
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      CERTIFICATE_BUCKET = var.bucket_name
      CERTIFICATE_TABLE  = var.dynamodb_table_name
    }
  }
}
