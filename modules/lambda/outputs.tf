output "lambda_function_name" {
  value = aws_lambda_function.certificate_parser.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.certificate_parser.arn
}
