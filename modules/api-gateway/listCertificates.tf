resource "aws_api_gateway_method" "get_certificates" {
  rest_api_id   = aws_api_gateway_rest_api.certificate_api.id
  resource_id   = aws_api_gateway_resource.certificates.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_certificates_integration" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  resource_id = aws_api_gateway_resource.certificates.id
  http_method = aws_api_gateway_method.get_certificates.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.list_certificates_lambda_invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_list" {
  statement_id  = "AllowAPIGatewayInvokeList"
  action        = "lambda:InvokeFunction"
  function_name = var.list_certificates_lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.certificate_api.execution_arn}/*/*"
}
