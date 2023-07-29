import json
import boto3

from decouple import config

client = boto3.client("lambda")
import requests


def lambda_handler(event, context):


    params1 = {"queryStringParameters": {"file_name": "videoplayback.mp4"}}
    params2 = {"queryStringParameters": {"file_name": "audio1.wav"}}

    res1 = client.invoke(
        FunctionName = config("EXPRESSIONARN"),
        InvocationType = "Event",
        Payload = json.dumps(params1)
    )

    res2 = client.invoke(
        FunctionName = config("AUDIOARN"),
        InvocationType = "Event",
        Payload = json.dumps(params2)
    )
    try:
        ExpressionRes = json.load(res1["Payload"]) 
        AudioRes = json.load(res2["Payload"])
    except:
        return{
            "statusCode": 400,
            "body": json.dumps({
                "Message": "File not found"
            })
        } 

    return {
        "statusCode": 200,
        "body": json.dumps({
            "ExpressionResponse": ExpressionRes,
            "AudioResponse": AudioRes
        }),
    }
