data "archive_file" "parser_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src/parser"
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

# Permission for S3 to invoke Lambda
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.certificate_parser.arn
  principal     = "s3.amazonaws.com"
}

# S3 Bucket Notification to trigger parser Lambda
resource "aws_s3_bucket_notification" "certificate_parser_trigger" {
  bucket = var.bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.certificate_parser.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".pdf" 
  }

  depends_on = [aws_lambda_permission.allow_s3]
}
