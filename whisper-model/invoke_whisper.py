import boto3

aws_region='us-east-2'

# Create a low-level client representing Amazon SageMaker Runtime
sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=aws_region)

# Specify the location of the input. Here, a single SVM sample
input_location = "s3://whispbucket/Transcriber_test.wav"

# The name of the endpoint. The name must be unique within an AWS Region in your AWS account. 
endpoint_name='whisper-base'

# After you deploy a model into production using SageMaker hosting 
# services, your client applications use this API to get inferences 
# from the model hosted at the specified endpoint.
response = sagemaker_runtime.invoke_endpoint_async(
                            EndpointName=endpoint_name, 
                            InputLocation=input_location,
                            InvocationTimeoutSeconds=3600)


print(response)