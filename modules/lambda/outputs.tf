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

output "get_certificate_lambda_function_name" {
  value = aws_lambda_function.get_certificate.function_name
}

output "get_certificate_lambda_arn" {
  value = aws_lambda_function.get_certificate.arn
}
output "get_certificate_lambda_invoke_arn" {
  value = aws_lambda_function.get_certificate.invoke_arn
}
