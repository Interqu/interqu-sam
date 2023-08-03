import os
from dotenv import load_dotenv
import openai
import random
import json

load_dotenv()

# Initilizing openai with a given API_KEY.
openai.api_key = os.getenv('API_KEY')

model = "gpt-4"


# System
contentFeedbackPrompt = "You are a program named Interqu that analyzes interview answers. You will give feedback on an answer's structure, content and effectiveness and suggest improvements to stand out (give exmaples if possible). Use personal pronouns in your response and ensure the lengths of your response is between 200 words to 500 words. Start your feedback with {{In this interview, you've...}}. Please format as a JSON: {{Score:*score out of 100*, Description:*one word description of the interview*, Feedback:*feedback*}}"
visualFeedbackPrompt = "You will act as a professional interview coach, speak in a professional manner, and will ONLY anaylze the facial emotions of an interviewee. In this query, you are provided an array of facial emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words. Answer with the format: 'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"
audioFeedbackPrompt = "You will act as a professional interview coach, speak in a professional manner, and will ONLY anaylze the vocal emotions of an interviewee. In this query, you are provided an array of vocal emotions detected by our system every second (i.e each element is the emotion detected within the second). Ensure you refer to the interviewee directly using pronouns like 'you', and ensure the lengths of your response is max of 400 words. Answer with the format: 'In this interview, you've....{what the array shows}...{what emotions should be displayed}...{helpful advice}...'"


def generateFeedback(position, question, visualEmotions, audioEmotions, content):
    try:
        visualFeedback = generateVisualFeedback(
            position, question, visualEmotions)
        audioFeedback = generateAudioFeedback(
            position, question, audioEmotions)
        contentFeedback = json.loads(generateContentFeedback(
            position, question, content).replace('\n', ' ').replace('\r', ''))
        return json.dumps({"videoAnalysis": visualFeedback,
                           "audioAnalysis": audioFeedback,
                           "contentOverall": contentFeedback['Score'],
                           "contentScore": contentFeedback['Description'],
                           "contentAnalysis": contentFeedback['Feedback']
                           })
    except Exception as error:
        print(error)
        # TODO implement proper error handling here
        print("An error has occured")


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

# FOR TESTING PURPOSELY ONLY


def generateFacialEmotionArray(interviewLength):
    emotions = ['anger', 'sadness', 'fear',
                'disgust', 'happy', 'surprised', 'neutral']
    dominant = emotions[random.randint(0, 6)]
    answer = []
    for x in range(0, interviewLength):
        ran = random.randint(0, 100)
        if ran > 50:
            answer.append(emotions[random.randint(0, 6)])
        else:
            answer.append(dominant)
    return answer

# Example
#print(generateFeedback("Software Engineer", "Tell me a time you failed.", generateFacialEmotionArray(45), generateFacialEmotionArray(45), "Well, I believe failure is a part of life, and it's through those experiences that we learn and grow. One significant time I experienced failure was during a project at my previous job. We were tasked with developing a new product, and I was leading the team. In the early stages of the project, I underestimated the complexity of the task and overestimated the team's capabilities. As a result, we faced significant delays, missed deadlines, and the final product didn't meet the quality standards we had aimed for. It was a tough pill to swallow as I had put in a lot of effort and wanted the project to succeed. However, I didn't let this failure define me or the team. Instead, I took responsibility for my mistakes and initiated a post-mortem analysis to understand what went wrong. We identified areas for improvement, such as better planning, allocating resources more effectively, and enhancing communication within the team. Learning from that experience, I implemented changes in my approach to project management. I became more attentive to the team's needs, encouraged open feedback, and created a more supportive and collaborative environment. The subsequent projects I led showed significant improvements, and we achieved better results. Failure taught me the importance of resilience, adaptability, and humility. I now approach challenges with a growth mindset, and I'm not afraid to seek help or advice from others when needed. Overall, that failure turned out to be a valuable learning experience, and it has made me a better professional and leader today."))
