import pymongo  
import urllib.parse
import os
import json
from datetime import datetime, timezone, timedelta

mongourl = os.environ.get('MONGODB_URL')
client = pymongo.MongoClient(mongourl)
db = client["interqu"] 
collection = db["interview_results"]


def lambda_handler(event, context):
    results = event[0]["analysis_result"]

    analysis = {
        "overall":{
            "overall": 10,
            "overall_summary": "Lorem Ipsum"
        },
        "video": {
            "video_score": results["video_score"],
            "video_timestamps": json.loads(results["video_emotion_array"])["output"]["Timeline"],
            "video_feedback": results["video_feedback"]
        },
        "audio": {
            "audio_score": results["audio_score"],
            "audio_timestamps": json.loads(results["audio_emotion_array"])["predictions"],
            "audio_feedback": results["audio_feedback"]
        },
        "context": {
            "content_score": results["content_score"],
            "transcript": results["transcript"],
            "context_feedback": results["content_analysis"]
        }
    }

    
    payload = {
        "question_id": event[0]["body"]["question_id"],
        "user_id": event[0]["body"]["user_id"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": analysis,
        "_class": "com.interqu.interviews.Result"
    }

    try:
        collection.insert_one(payload)

        return {
            'statusCode': 200
        }
        
    except pymongo.errors.PyMongoError as e:
        return{
            'statusCode': 500
        }