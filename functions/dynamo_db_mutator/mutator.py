import requests
import json
import os

client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f"dynamo mutator, event received: {event}")

    url = os.getenv("APPSYNC_URL", "")
    execution_arn = event["detail"]["executionArn"]
    inputs = json.loads(event['detail']['input'])

    response = client.get_execution_history(executionArn=execution_arn)

    # Assuming you want the latest event which should be the last in the list
    latest_event = response["events"][-1]
    state_name = latest_event.get("stateEnteredEventDetails", {}).get("name")

    print("Current State Name:", state_name)

    query = """
    mutation updateVideoProcessing($input: UpdateVideoProcessingInput!) {
        updateVideoProcessing(input: $input) {
            Connection_id
            Interview_id
            Progress
        }
    }
    """

    variables = {"Connection_id": inputs['user-id'], "Interview_id": inputs['interview-id'], "Progress": state_name}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            url,
            headers=headers,
            json={"query": query, "variables": json.dumps(variables)},
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
