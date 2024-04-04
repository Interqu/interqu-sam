import boto3
import json


def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("WebSocketConnections")  # Replace with your table name

    # API Gateway management client setup
    client = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url="https://<api-id>.execute-api.<region>.amazonaws.com/prod",
    )  # Fill in your API Gateway endpoint

    # Fetch connection IDs from DynamoDB
    connections = table.scan()["Items"]

    # The message to send - customize based on your application's needs
    message = {
        "action": "sendMessage",
        "data": "State update message",  # Customize this message
    }

    for connection in connections:
        connection_id = connection["connectionId"]
        try:
            # Send message to the client
            client.post_to_connection(
                ConnectionId=connection_id, Data=json.dumps(message)
            )
        except client.exceptions.GoneException:
            # Handle the case where the connection is no longer available
            print(f"Connection ID {connection_id} is gone, removing from database...")
            table.delete_item(Key={"connectionId": connection_id})

    return {"statusCode": 200, "body": json.dumps("Messages sent successfully")}
