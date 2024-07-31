module "s3" {
  source = "./modules/s3"
}

module "iam" {
  source          = "./modules/iam"
  s3_bucket_arn   = module.s3.bucket_arn
  s3_bucket_name  = module.s3.bucket_name
}

module "sagemaker" {
  source          = "./modules/sagemaker"
  s3_bucket_name  = module.s3.bucket_name
  execution_role_arn = module.iam.execution_role_arn
}
