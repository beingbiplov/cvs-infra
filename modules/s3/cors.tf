resource "aws_s3_bucket_cors_configuration" "certificate_bucket_cors" {
  bucket = aws_s3_bucket.certificate_bucket.id

  cors_rule {
    allowed_methods = ["PUT", "POST", "GET"]
    allowed_origins = ["*"]
    allowed_headers = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
