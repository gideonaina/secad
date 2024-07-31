resource "aws_s3_bucket" "model_bucket" {
  bucket = "llama-model-bucket"
}

output "bucket_name" {
  value = aws_s3_bucket.model_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.model_bucket.arn
}
