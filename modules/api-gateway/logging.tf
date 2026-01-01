resource "aws_api_gateway_account" "apigateway_account" {
  cloudwatch_role_arn = aws_iam_role.apigateway_cloudwatch_role.arn
}

resource "aws_cloudwatch_log_group" "apigw_logs" {
  name              = "/aws/apigateway/cert-verification-${var.environment}"
  retention_in_days = 14
}

resource "aws_api_gateway_stage" "stage" {
  stage_name    = var.environment
  rest_api_id   = aws_api_gateway_rest_api.certificate_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.apigw_logs.arn
    format = jsonencode({
      requestId = "$context.requestId"
      httpMethod = "$context.httpMethod"
      resourcePath = "$context.resourcePath"
      status = "$context.status"
      error = "$context.error.message"
    })
  }
}
