import os
import openai
import json

# Initilizing openai with a given API_KEY.
openai.api_key = os.environ.get('OPENAI_API_KEY')

model = "gpt-4"


# System
contentFeedbackPrompt = "You are a program named Interqu that analyzes interview answers. You will give feedback on an answer's structure, content and effectiveness and suggest improvements to stand out (give exmaples if possible). Use personal pronouns in your response and ensure the lengths of your response is between 200 words to 500 words. Start your feedback with {{In this interview, you've...}}. Please format as a JSON: {{Score:*score out of 100*, Description:*one word description of the interview*, Feedback:*feedback*}}"
visualFeedbackPrompt = "You will act as a professional interview coach, speak in a professional manner, and will ONLY anaylze the facial emotions of an interviewee. In this query, you are provided an array of facial emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words. Answer with the format: 'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"
audioFeedbackPrompt = "You will act as a professional interview coach, speak in a professional manner, and will ONLY anaylze the vocal emotions of an interviewee. In this query, you are provided an array of vocal emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words. Answer with the format: 'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"


def lambda_handler(event, context):
    feedback = generateFeedback(event["questionId"], event["userId"],
                                event["position"], event["question"], event["visualEmotions"], event["audioEmotions"], event["content"])
    return feedback


def generateFeedback(questionId, userId, position, question, visualEmotions, audioEmotions, content):
    try:
        visualFeedback = generateVisualFeedback(
            position, question, visualEmotions)
        audioFeedback = generateAudioFeedback(
            position, question, audioEmotions)
        contentFeedback = json.loads(generateContentFeedback(
            position, question, content).replace('\n', ' ').replace('\r', ''))
        return json.dumps({"statusCode": 200,
                           "body": {"questionId": questionId,
                                    "userId": userId},
                           "analysisResult": {
                               "videoAnalysis": visualFeedback,
                               "audioAnalysis": audioFeedback,
                               "contentOverall": contentFeedback['Score'],
                               "contentScore": contentFeedback['Description'],
                               "contentAnalysis": contentFeedback['Feedback']
                           }
                           })
    except Exception as error:
        print(error)
    return {
        "statusCode": 500,
        "body": json.dumps(
            {
                "error": "an error has occured generating feedback",
            }
        ),
    }


def generateContentFeedback(position, question, answer):
    # Answer Query DO NOT CHANGE OPTIMIZED QUERY
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": contentFeedbackPrompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Answer:'{answer}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return query['choices'][0]['message']['content']
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")


def generateVisualFeedback(position, question, analyzedVideoContent):
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": visualFeedbackPrompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Answer:'{analyzedVideoContent}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return query['choices'][0]['message']['content']
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")


def generateAudioFeedback(position, question, analyzedVideoContent):
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": audioFeedbackPrompt},
            {"role": "user", "content": f"This is an interview for a {position} position. Question:'{question}'. Answer:'{analyzedVideoContent}'"}
        ]
    )
    # Validating answer
    finish_reason = query['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        return query['choices'][0]['message']['content']
    raise Exception(
        f"UNEXPECTED ERROR. Response Generation could not complete. Finish Reason: {finish_reason}")
