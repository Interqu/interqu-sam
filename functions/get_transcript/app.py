import boto3
import json
import time
import pandas as pd

client = boto3.client('transcribe')
s3 = boto3.client('s3')


def lambda_handler(event, context):


    file_name = event[0]["audio"]["file_id"]
    if not file_name:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "no file name was provided",
                }
            ),
        }
    
    audio_file=file_name
    audio_file=file_name
    output_file=file_name+".json"

    
    job_list = client.list_transcription_jobs()
    for job in job_list['TranscriptionJobSummaries']:
        if file_name == job['TranscriptionJobName']:
            client.delete_transcription_job(
                TranscriptionJobName=file_name
            )

    response = client.start_transcription_job(
    TranscriptionJobName=file_name,
    LanguageCode='en-US',
    MediaFormat='wav',
    Media={
        'MediaFileUri': 's3://interqu-audio/{}'.format(audio_file),
    },
    OutputBucketName='interqu-audio',
    OutputKey=output_file
    # JobExecutionSettings={
    #     'AllowDeferredExecution': True,
    #     'DataAccessRoleArn': 'string'
    # }
    )



    while True:
        result = client.get_transcription_job(TranscriptionJobName=file_name)
        if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(15)

    if result['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
        s3.download_file("interqu-audio", output_file, "/tmp/"+output_file)
        data = pd.read_json("/tmp/"+output_file)
        return {
            "statusCode": 200,
            "body":data['results']['transcripts'][0]['transcript']
        }
        return {
            "statusCode": 200,
            "body":data['results']['transcripts'][0]['transcript']
        }
    else:
        return {
            "statusCode": 418,
            "body": json.dumps(
                {
                    "error": "transcription failed",
                    "Failure Reason": result['TranscriptionJob']['FailureReason'],
                }
            ),
        }
