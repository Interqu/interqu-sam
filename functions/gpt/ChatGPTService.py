import os
import openai
import json
import logging

# Initilizing openai with a given API_KEY.
openai.api_key = os.environ.get('OPENAI_API_KEY')

model = "gpt-4-turbo-preview"


# System
content_feedback_prompt = "You are a program named Interqu that analyzes interview answers. You will give feedback on an answer's structure, content and effectiveness and suggest improvements to stand out (give exmaples if possible). Use our professional guide as reference (tips, what employers look for, and what to avoid mentioning during the interview). Use personal pronouns in your response and ensure the lengths of your response is between 200 miniumwords to 500 words. Start your feedback with {{In this interview, you've...}}. Please format as a JSON: {{score:*score out of 100*, feedback:*feedback*}}"
visual_feedback_prompt = "You will act as a professional interview coach, named Interqu, speak in a professional manner, and will ONLY anaylze the facial emotions of an interviewee. Do not mention anything about the content of the interview just emotion. In this query, you are provided an array of facial emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words and minimun 200 words. Answer with the JSON format: 'feedback':'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"
audio_feedback_prompt = "You will act as a professional interview coach, named Interqu, speak in a professional manner, and will ONLY anaylze the vocal emotions of an interviewee.  Do not mention anything about the content of the interview just emotion. In this query, you are provided an array of vocal emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words and minimin 200 words. Answer with the JSON format: 'feedback': 'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"

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
    logging.info(f"gpt analysis triggered with event: {event}")
    feedback = generate_feedback(event["question_id"], event["user_id"],
                                event["position"], event["question"], event["tips"], event["employers_look_for"], event["avoid_mention"], event["visual_emotions"], event["audio_emotions"], event["visual_score"], event["audio_score"], event["transcript"])
    return feedback

# Returns obj to be stored in database
def generate_feedback(question_id, user_id, position, question, tips, employers_look_for, avoid_mention, visual_emotions, audio_emotions, visual_score, audio_score, transcript):
    try:
        visual_feedback = generate_visual_feedback(
            position, question, visual_emotions)
        audio_feedback = generate_audio_feedback(
            position, question, audio_emotions)
        content_feedback = generate_content_feedback(
            position, question, tips, employers_look_for, avoid_mention, transcript)
        return json.dumps({"status_code": 200,
                           "body": {"question_id": question_id,
                                    "user_id": user_id},
                           "analysis_result": {
                               "video_emotion_array": visual_emotions,
                               "audio_emotion_array": audio_emotions,
                               "video_score": visual_score,
                               "audio_score": audio_score,
                               "video_feedback": visual_feedback['feedback'],
                               "audio_feedback": audio_feedback['feedback'],
                               "content_score": content_feedback['score'],
                               "content_analysis": content_feedback['feedback'],
                               "transcript": transcript
                           }
                           })
    except Exception as error:
        logging.error(f"GPT analysis error: {error}")
    return {
        "statusCode": 500,
        "body": json.dumps(
            {
                "error": "an error has occured generating feedback",
            }
        ),
    }


def generate_content_feedback(position, question, tips, employers_look_for, avoid_mention, answer):
    # Answer Query DO NOT CHANGE OPTIMIZED QUERY
    query = openai.ChatCompletion.create(
        model=model,
        response_format={"type":"json_object"},
        messages=[
            {"role": "system",
                "content": content_feedback_prompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Tips: '{tips}'. Employers Look For: '{employers_look_for}'. Avoid Mentioning: '{avoid_mention}'. Answer:'{answer}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return json.loads(query['choices'][0]['message']['content'])
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")


def generate_visual_feedback(position, question, processed_video_emotions):
    query = openai.ChatCompletion.create(
        model=model,
        response_format={"type":"json_object"},
        messages=[
            {"role": "system",
                "content": visual_feedback_prompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Answer:'{processed_video_emotions}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return json.loads(query['choices'][0]['message']['content'])
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")


def generate_audio_feedback(position, question, processed_video_sentiment):
    query = openai.ChatCompletion.create(
        model=model,
        response_format={"type":"json_object"},
        messages=[
            {"role": "system",
             "content": audio_feedback_prompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Answer:'{processed_video_sentiment}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return json.loads(query['choices'][0]['message']['content'])
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")