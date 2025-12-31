data "archive_file" "parser_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/parser_lambda.zip"
}

# Certificate Parser Lambda Function
resource "aws_lambda_function" "certificate_parser" {
  function_name = "${var.project_name}-${var.environment}-certificate-parser"
  runtime       = "python3.11"
  handler       = "parser_handler.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  filename         = data.archive_file.parser_lambda_zip.output_path
  source_code_hash = data.archive_file.parser_lambda_zip.output_base64sha256

  environment {
    variables = {
      CERTIFICATE_BUCKET = var.bucket_name
      CERTIFICATE_TABLE  = var.dynamodb_table_name
    }
  }
}
