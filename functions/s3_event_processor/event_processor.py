import boto3
import json
import os

# Initialize clients
s3 = boto3.client('s3')
sfn = boto3.client('stepfunctions')

STATE_MACHINE_ARN = os.environ['STATEMACHINE_ARN']

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
        user_id = response['Metadata'].get('user-id', 'Unknown')
        question_id = response['Metadata'].get('question-id', 'Unknown')
        input_data['user-id'] = user_id
        input_data['question-id'] = question_id
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('Error getting file metadata, cannot identify user-id')
        }

    # Start execution of the state machine
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(input_data)
    )

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps('State Machine Execution Started Successfully')
    }
