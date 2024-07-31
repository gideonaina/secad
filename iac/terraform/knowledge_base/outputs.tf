output "endpoint_url" {
  value = "https://runtime.sagemaker.${var.region}.amazonaws.com/endpoints/${module.sagemaker.endpoint_name}/invocations"
}