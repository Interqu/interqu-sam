import datetime
import boto3
from time import gmtime, strftime

aws_region='us-east-2'

sagemaker_client = boto3.client('sagemaker', region_name=aws_region)

sagemaker_role = "---------------------------------------"

s3_bucket = 'whispbucket'
bucket_prefix =''
model_s3_key = f"whisper-model.tar.gz"

model_url = f"s3://{s3_bucket}/{model_s3_key}"

from sagemaker import image_uris

model_name = 'whisper-base-english-2'



# Create an endpoint config name. Here we create one based on the date  
# so it we can search endpoints based on creation time.
endpoint_config_name = f"whisperEndpointConfig-{strftime('%Y-%m-%d-%H-%M-%S', gmtime())}"

# The name of the model that you want to host. This is the name that you specified when creating the model.
model_name='whisper-base-english'

create_endpoint_config_response = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name, # You will specify this name in a CreateEndpoint request.
    # List of ProductionVariant objects, one for each model that you want to host at this endpoint.
    ProductionVariants=[
        {
            "VariantName": "variant1", # The name of the production variant.
            "ModelName": model_name, 
            "InstanceType": "ml.t2.medium", # Specify the compute instance type.
            "InitialInstanceCount": 1 # Number of instances to launch initially.
        }
    ],
    AsyncInferenceConfig={
        "OutputConfig": {
            # Location to upload response outputs when no location is provided in the request.
            "S3OutputPath": f"s3://{s3_bucket}/output"
        },
        "ClientConfig": {
            # (Optional) Specify the max number of inflight invocations per instance
            # If no value is provided, Amazon SageMaker will choose an optimal value for you
            "MaxConcurrentInvocationsPerInstance": 5
        }
    }
)

print(f"Created EndpointConfig: {create_endpoint_config_response['EndpointConfigArn']}")

# The name of the endpoint.The name must be unique within an AWS Region in your AWS account.
endpoint_name = 'whisper-base-2' 

# The name of the endpoint configuration associated with this endpoint.
endpoint_config_name=endpoint_config_name

create_endpoint_response = sagemaker_client.create_endpoint(
                                            EndpointName=endpoint_name, 
                                            EndpointConfigName=endpoint_config_name) 
                                            
