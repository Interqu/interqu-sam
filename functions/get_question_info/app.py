import pymongo  
import urllib.parse
import os
import json

mongourl = os.environ.get('MONGODB_URL')
client = pymongo.MongoClient(mongourl) 
db = client["interqu"]
collection = db["interview_questions"] 


def lambda_handler(event, context):
    try:
        questionBody = collection.find_one({"question_id": event[1]["question_id"]})
        questionBody["_id"] = str(questionBody["_id"])
        out = {
            'statusCode': 200,
            'user_id': event[1]["user_id"],
            'question_body': questionBody
        }
        return out
        
    except pymongo.errors.PyMongoError as e:
        return{
            'statusCode': 500
        }