import os
import json
import logging
from pymongo import MongoClient
from urllib.parse import quote_plus

mongoURI = f"mongodb+srv://al.x.300000@gmail.com:W54ce97Vj^@cluster0.eoyfjou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(mongoURI)
db = client["interqu"]
collection = db["interview_questions"]

# Input:
# question_id - question id of the interview : string
# user_id - user id that took the interview : string
# position - position in english, of the interview : string
# question - the question in english of the interview : string
# tips - five tips on how to answer this question  : string[]
# employers_look_for - five points of what employers look for in this question : string[]
# avoid_mention - five things you should not mention : string[]
# visual_emotions - visual emotions from GetExpression() : string[]
# audio_emotions - audio emotions from GetSentiment() : string[]
# visual_score - visual score from GetExpression() : number
# audio_score - audio score from GetSentiment() : number
# transcript - transcript of the interview. : string
def lambda_handler(event, context):
    question = collection.find_one({"question_id" : event["question_id"]})
    print(question)
    return
