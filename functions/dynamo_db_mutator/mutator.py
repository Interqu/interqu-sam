def lambda_handler(event, context):
    print(f"dynamo mutator, event received: {event}")

    return {
        "statusCode": 200,
        "body": {
            "error": "successfully modified dynamo table entry",
        },
    }