import requests
import json

client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f"dynamo mutator, event received: {event}")

    url = "https://your-appsync-api-url.amazonaws.com/graphql"
    api_key = "your-appsync-api-key"
    execution_arn = event["detail"]["executionArn"]

    response = client.get_execution_history(executionArn=execution_arn)

    # Assuming you want the latest event which should be the last in the list
    latest_event = response["events"][-1]
    state_name = latest_event.get("stateEnteredEventDetails", {}).get("name")

    print("Current State Name:", state_name)

    query = """
    mutation UpdateProduct($id: ID!, $name: String!) {
        updateProduct(id: $id, name: $name) {
            id
            name
        }
    }
    """

    variables = {"id": "123", "name": "New Product Name"}

    headers = {"Content-Type": "application/json", "x-api-key": api_key}

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
