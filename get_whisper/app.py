import boto3
import json
import whisper
import os

s3 = boto3.client('s3')


def lambda_handler(event, context):

    file_name = event["queryStringParameters"]["audio_file"]
    if not file_name:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "no file name was provided",
                }
            ),
        }
    
    audio_file=file_name+".wav"
    print(audio_file)
    s3.download_file("interqu-audio", audio_file, "../tmp/audio.wav")


    print(os.getcwd())
    print("---------------------------------------------------------------------------------------")

    print(os.listdir())
    print("---------------------------------------------------------------------------------------")

    print(os.listdir("../tmp"))

    print("---------------------------------------------------------------------------------------")

    thisdir = os.getcwd()

    # r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(".wav"):
                print(os.path.join(r, file))


    target_name = event["queryStringParameters"]["target_name"]
    model = whisper.load_model("medium")
    result = model.transcribe(target_name)


    print(result["text"])
    return(result["text"])
