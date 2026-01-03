resource "aws_api_gateway_resource" "certificate_id" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  parent_id   = aws_api_gateway_resource.certificates.id
  path_part   = "{certificateId}"
}

resource "aws_api_gateway_method" "get_certificate" {
  rest_api_id   = aws_api_gateway_rest_api.certificate_api.id
  resource_id   = aws_api_gateway_resource.certificate_id.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_certificate_integration" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  resource_id = aws_api_gateway_resource.certificate_id.id
  http_method = aws_api_gateway_method.get_certificate.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.get_certificate_lambda_invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_get" {
  statement_id  = "AllowAPIGatewayInvokeGetCertificate"
  action        = "lambda:InvokeFunction"
  function_name = var.get_certificate_lambda_function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.certificate_api.execution_arn}/*/GET/certificates/*"
}

resource "aws_api_gateway_method" "options_certificate_id" {
  rest_api_id   = aws_api_gateway_rest_api.certificate_api.id
  resource_id   = aws_api_gateway_resource.certificate_id.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_certificate_id" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  resource_id = aws_api_gateway_resource.certificate_id.id
  http_method = aws_api_gateway_method.options_certificate_id.http_method

  type = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options_certificate_id_200" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  resource_id = aws_api_gateway_resource.certificate_id.id
  http_method = aws_api_gateway_method.options_certificate_id.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_integration_response" "options_certificate_id_200" {
  rest_api_id = aws_api_gateway_rest_api.certificate_api.id
  resource_id = aws_api_gateway_resource.certificate_id.id
  http_method = aws_api_gateway_method.options_certificate_id.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
  }
}


