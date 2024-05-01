import requests
import json
import os
import boto3
from requests_aws_sign import AWSV4Sign

client = boto3.client("stepfunctions")


def lambda_handler(event, context):

    print(f"dynamo mutator, event received: {event}")

    url = os.getenv("APPSYNC_URL", "")
    execution_arn = event["detail"]["executionArn"]
    inputs = json.loads(event['detail']['input'])

    response = client.get_execution_history(executionArn=execution_arn, reverseOrder=True)
    print(f"execution event: {response}")

    # Assuming you want the latest event which should be the last in the list
    latest_event = response["events"][-1]
    state_name = latest_event.get("stateEnteredEventDetails", {}).get("name")

    print("Current State Name:", state_name)

    session = boto3.session.Session()
    credentials = session.get_credentials()

    
    auth=AWSV4Sign(credentials, "us-east-1", 'appsync')

    mutation = """
    mutation updateVideoProcessing($input: UpdateVideoProcessingInput!) {
        updateVideoProcessing(input: $input) {
            Connection_id
            Interview_id
            Progress
        }
    }
    """
    input_data = {
        "input": {
            "Connection_id": inputs['user-id'],
            "Interview_id": inputs['interview-id'],
            "Progress": state_name
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url,
            auth=auth,
            json={"query": mutation, "variables": json.dumps(input_data)},
            headers=headers
        )

        print(f"Mutate success! Response: {response}")
    except Exception as e:
        print(f"failed to mutate dynamo db entry: {e}")
        return

    return {
        "statusCode": 200,
        "body": {
            "text": "successfully modified dynamo table entry",
        },
    }
