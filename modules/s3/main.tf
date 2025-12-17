resource "aws_s3_bucket" "certificate_bucket" {
  bucket = "${var.project_name}-${var.environment}-certificates"
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket = aws_s3_bucket.certificate_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
