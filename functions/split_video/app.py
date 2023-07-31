import json
import boto3
import requests

client = boto3.client("lambda")

def lambda_handler(event, context):
    event = event['Input']
    final_json = str()
    
    s3 = boto3.resource('s3')
    bucket = event['bucket'].split(':')[-1]
    filename = event['key']
    directory = "/tmp/{}".format(filename)
    
    s3.Bucket(bucket).download_file(filename, directory)
    
    with open(directory, "r") as jsonfile:
        final_json = json.load(jsonfile)
    
    os.popen("rm -rf /tmp")
    
    return final_json

    
