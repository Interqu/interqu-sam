import boto3

aws_region='us-east-2'

sagemaker_client = boto3.client('sagemaker', region_name=aws_region)

sagemaker_role = "---------------------------------"

s3_bucket = 'whispbucket'
bucket_prefix =''
model_s3_key = f"whisper-model.tar.gz"

model_url = f"s3://{s3_bucket}/{model_s3_key}"

from sagemaker import image_uris

container = image_uris.retrieve(region=aws_region, framework='pytorch', image_scope='inference', version='1.12', instance_type='ml.t2.medium')

model_name = 'whisper-base-english'

create_model_response = sagemaker_client.create_model(
    ModelName = model_name,
    ExecutionRoleArn = sagemaker_role,
    PrimaryContainer = {
        'Image' : container,
        'ModelDataUrl' : model_url,
    }
)