import boto3
import json
import os

# Initialize clients
s3 = boto3.client('s3')
sfn = boto3.client('stepfunctions')

STATE_MACHINE_ARN = os.environ['STATEMACHINE_ARN']
METADATA_FIELDS = ['user-id', 'question-id', 'interview-id']
# METADATA_PREFIX = 'x-amz-meta-'

def lambda_handler(event, context):
    # logging
    print("Event Received: ", event)

    # Assuming only one record is present
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    # input data for statemachine
    input_data = {
        "bucket": bucket_name,
        "file_id": object_key
    }

    try:
        # Retrieve metadata from the object
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        print(f'Object metadata recieved: {response["Metadata"]}')

        for field in METADATA_FIELDS:
            input_data[field] = response['Metadata'][field]
            if not input_data[field]:
                raise ValueError(f"Missing metadata {field}")

    except Exception as e:
        # for logging
        print(f'could not fetch metadata, received error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error getting file metadata: {e}')
        }

    # Start execution of the state machine
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(input_data)
    )

    # Return the response
    print(f"Statemachine successfully started for file: {object_key}")
    return {
        'statusCode': 200,
        'body': json.dumps('State Machine Execution Started Successfully')
    }
