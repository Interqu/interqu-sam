import boto3
import time

aws_region='us-east-1'

sagemaker_client = boto3.client('sagemaker', region_name=aws_region)

sagemaker_role = "---------------------------------"

s3_bucket = 'whispbucket'
bucket_prefix =''
model_s3_key = f"whisper-model.tar.gz"

model_url = f"s3://{s3_bucket}/{model_s3_key}"

from sagemaker import image_uris
import sagemaker

container = image_uris.retrieve(region=aws_region, framework='pytorch', image_scope='inference', version='1.12', instance_type='ml.t2.medium')

model_name = 'whisper-base-english-2'


model_name = f'whisper-model-{int(time.time())}'
whisper_model_sm = sagemaker.model.Model(
    model_data=model_url,
    image_uri=container,
    role=sagemaker_role,
    entry_point="inference.py",
    source_dir='src',
    name=model_name,
)

endpoint_name = f'whisper-endpoint-{int(time.time())}'
whisper_model_sm.deploy(
    initial_instance_count=1,
    instance_type="ml.t2.medium",
    endpoint_name=endpoint_name,
    wait=True,
    ServerlessInferenceConfig={
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

print(endpoint_name)