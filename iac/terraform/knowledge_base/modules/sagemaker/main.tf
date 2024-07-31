resource "aws_sagemaker_model" "model" {
  name               = "Llama3-1-70B"
  execution_role_arn = var.execution_role_arn

  primary_container {
    image          = "amazonaws.com/bedrock/llama:3.1-70B"
    model_data_url = "s3://${var.s3_bucket_name}/path-to-your-model-data"
  }
}

resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = "Llama3-1-70B-Endpoint-Config"

  production_variants {
    variant_name          = "AllTraffic"
    model_name            = aws_sagemaker_model.model.name
    initial_instance_count = 1
    instance_type         = "ml.p3.16xlarge" # Update as needed
  }
}

resource "aws_sagemaker_endpoint" "endpoint" {
  name                  = "Llama3-1-70B-Endpoint"
  endpoint_config_name  = aws_sagemaker_endpoint_configuration.endpoint_config.name
}

output "endpoint_name" {
  value = aws_sagemaker_endpoint.endpoint.name
}
