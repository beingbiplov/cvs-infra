output "lambda_function_name" {
  value = aws_lambda_function.certificate_presign.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.certificate_presign.arn
}

output "invoke_arn" {
  value = aws_lambda_function.certificate_presign.invoke_arn
}

output "parser_lambda_function_name" {
  value = aws_lambda_function.certificate_parser.function_name
}

output "parser_lambda_arn" {
  value = aws_lambda_function.certificate_parser.arn
}

output "parser_lambda_invoke_arn" {
  value = aws_lambda_function.certificate_parser.invoke_arn
}