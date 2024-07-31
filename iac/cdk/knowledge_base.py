from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    core
)

class BedrockLlamaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Parameters
        model_name = "Llama3_1_70B"
        endpoint_name = "Llama3_1_70B_Endpoint"
        instance_type = "ml.p3.16xlarge"
        s3_bucket_name = "llama-model-bucket"

        # S3 Bucket
        s3_bucket = s3.Bucket(self, "ModelBucket", bucket_name=s3_bucket_name)

        # IAM Role
        execution_role = iam.Role(self, "ExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
            ]
        )

        # SageMaker Model
        model = sagemaker.CfnModel(self, "Model",
            execution_role_arn=execution_role.role_arn,
            model_name=model_name,
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image="amazonaws.com/bedrock/llama:3.1-70B",
                model_data_url=f"s3://{s3_bucket.bucket_name}/path-to-your-model-data"
            )
        )

        # SageMaker Endpoint Configuration
        endpoint_config = sagemaker.CfnEndpointConfig(self, "EndpointConfig",
            endpoint_config_name=endpoint_name,
            production_variants=[sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                model_name=model.model_name,
                variant_name="AllTraffic",
                initial_instance_count=1,
                instance_type=instance_type
            )]
        )

        # SageMaker Endpoint
        sagemaker.CfnEndpoint(self, "Endpoint",
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config.endpoint_config_name
        )

        # Output the Endpoint URL
        core.CfnOutput(self, "EndpointUrl",
            value=f"https://runtime.sagemaker.{core.Aws.REGION}.amazonaws.com/endpoints/{endpoint_name}/invocations",
            description="The URL of the deployed endpoint."
        )

app = core.App()
BedrockLlamaStack(app, "BedrockLlamaStack")
app.synth()
