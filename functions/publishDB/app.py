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
            "overall_score": 10,
            "overall_summary": results["overall_feedback"]
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
        "file_id": event[1][4][1]["file_id"],
        "video_length": len(json.loads(results["video_emotion_array"])["output"]["Timeline"]) * 2,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": analysis,
        "interview_id": event[0]["body"]["interview_id"],
        "status": "DONE",
        "_class": "com.interqu.interviews.Result"
    }

    try:
        query = {"interview_id": event[0]["body"]["interview_id"]} 
        collection.replace_one(query, payload, upsert=True)

        return {
            'statusCode': 200
        }
        
    except pymongo.errors.PyMongoError as e:
        return{
            'statusCode': 500
        }