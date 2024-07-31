terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket-prod"
    key    = "path/to/prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

module "main" {
  source = "../../.."
}
