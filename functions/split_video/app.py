import boto3
import os
from moviepy.editor import VideoFileClip

client = boto3.client("lambda")

def extractAudio(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library"""

    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    print("writing file: " + filename)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


def lambda_handler(event, context):
    event = event['Input']
    final_json = str()
    
    s3 = boto3.resource('s3')
    bucket = event['bucket'].split(':')[-1]
    filename = event['key']
    directory = "/tmp/{}".format(filename)

    print("Downloading file: " + filename)
    s3.Bucket(bucket).download_file(filename, directory)

    # extract audio
    extractAudio(directory)
        
    os.popen("rm -rf /tmp")
    
    return final_json

    
