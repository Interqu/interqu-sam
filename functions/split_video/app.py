import boto3
import os
from moviepy.editor import VideoFileClip
import logging
from botocore.exceptions import ClientError

client = boto3.client("lambda")

def extractAudio(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library

    :return: filepath of where audio file was written
    """

    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    print("writing file: " + filename)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")

    return f"{filename}.{output_ext}"


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def lambda_handler(event, context):
    event = event['Input']
    final_json = str()
    
    s3 = boto3.resource('s3')
    bucket = event['bucket'].split(':')[-1]
    filename = event['key']
    directory = "/tmp/{}".format(filename)

    logging.info("Downloading file: " + filename)
    s3.Bucket(bucket).download_file(filename, directory)


    # extract audio
    logging.info("Extracting audio")
    filename = extractAudio(directory)


    # upload
    logging.info("Uploading audiofile")
    upload_file(filename, "interqu-audio")
        
    os.popen("rm -rf /tmp")
    
    return final_json

    
