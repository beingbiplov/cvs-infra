resource "aws_dynamodb_table" "certificates" {
  name         = "${var.project_name}-${var.environment}-certificates"
  billing_mode = var.billing_mode
  hash_key     = "certificateId"

  attribute {
    name = "certificateId"
    type = "S"
  }

  attribute {
  name = "userId"
  type = "S"
}

attribute {
  name = "createdAt"
  type = "S"
}

  global_secondary_index {
  name               = "userId-createdAt-index"
  hash_key           = "userId"
  range_key          = "createdAt"
  projection_type    = "ALL"
}

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Service     = "certification"
  }
}
