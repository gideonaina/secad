variable "s3_bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "execution_role_arn" {
  description = "The ARN of the execution role"
  type        = string
}
