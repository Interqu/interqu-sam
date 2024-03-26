import pymongo  
import urllib.parse
import os
import json
import datetime

mongourl = os.environ.get('MONGODB_URL')
client = pymongo.MongoClient(mongourl)
db = client["interqu"] 
collection = db["interview_results"]


def lambda_handler(event, context):

    
    
    payload = {
        "question_id": event[0]["body"]["question_id"],
        "user_id": event[0]["body"]["user_id"],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": event[0]["analysis_result"],
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