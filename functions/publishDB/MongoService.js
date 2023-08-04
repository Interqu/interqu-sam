const { MongoClient } = require("mongodb");

//TODO change with system env vars
const mongoURI = process.env.MONGODB_URL;
const dbName = "interqu";
const collectionName = "interview_result_data";

const javaDataClass = "com.interqu.interviews.InterviewVideoData";

export const lambdaHandler = async (event, context) => {
  const stock_price = event["stock_price"]; // example fetch data from event

  // Mocked result of a stock buying transaction

  let result = {
    "result" : "success/<anything else>"
  }


  return result;

};

//saves data to mongodb
async function saveDataToMongoDB(data) {
  const client = await MongoClient.connect(mongoURI);
  const db = client.db(dbName);
  const collection = db.collection(collectionName);
  await collection.insertOne(data);
  client.close();
}

//Prepares data to be saved to mongodb format
function prepareData(details, visualData, audioData, GPTDescription) {
  let interviewData = {
    questionId: details["questionId"],
    userId: details["userId"],
    dateTaken: details["dateTaken"],
    fileName: details["fileName"],
    videoLink: details["videoLink"],

    videoOverall: visualData["overall"], //String
    videoStats: visualData["stats"], //Array
    videoScore: visualData["score"], // Number
    videoAnalysis: GPTDescription["videoAnalysis"], //Generated text with GPT

    audioOverall: audioData["overall"],
    audioStats: audioData["stats"],
    audioScore: audioData["score"],
    audioAnalysis: GPTDescription["audioAnalysis"],

    contentOverall: GPTDescription["contentOverall"],
    contentScore: GPTDescription["contentScore"],
    contentAnalysis: GPTDescription["contentAnalysis"],

    _class: javaDataClass,
  };
  return interviewData;
}

//Call this method to save to database.
async function saveInterviewData(
  details,
  visualData,
  audioData,
  GPTDescription
) {
  let interviewData = prepareData(
    details,
    visualData,
    audioData,
    GPTDescription
  );

  try {
    await saveDataToMongoDB(interviewData);
    return "SUCCESS";
  } catch (e) {
    console.log(e);
    return "ERROR";
  }
}

//saveInterviewData(details, visualData, audioData, GPTDescription);

//Testing Variables
let details = {
  questionId: "a66b769f-3fe3-4c92-8178-c84e2a23013f", // String
  userId: "3927e291-7611-4060-a45a-8d2b15b7d5d0", // String
  dateTaken: "2023-02-01", //Date
  fileName: "asd[0oiq3hr-s0ad897fghwq32-9fg12-093gf2-fg2-8w9ef7gsd-897gf.mp4", //String
  videoLink: "http://interviews.interqu.com/interview_id_here", // String - a link to embedd in html - maybe add some security features for who can access this link
};

let visualData = {
  overall: "Neutral", // String - overall description like "neutral"
  stats: ["Neutral", "Neutral", "Neutral", "Happy"], // Array of VisualEmotions (String), one for each second of the video
  score: 69, //Integer - overall score like 67 out of 100
};

let audioData = {
  overall: "Angry", // String - overall description like "neutral"
  stats: ["Neutral", "Angry", "Angry", "Sadness"], // Array of AudioEmotions (String), one for each second of the video
  score: 33, //Integer - overall score like 67 out of 100
};

let GPTDescription = {
  videoAnalysis: `In this interview, you've shown a neutral facial expression for the majority of the time. While there were some moments of fear and surprise, it's important to remember that it's okay to show emotions during an interview. In fact, it can help convey your personality and provide a more human touch to the conversation. However, it's important to ensure that your emotions don't distract from the content of your answer.
  
    When answering the question about a time you failed, consider being transparent and authentic with your emotions. It's okay to show vulnerability, as it can demonstrate your honesty and self-awareness. It's important to remember to maintain a professional demeanor and ensure that your emotions don't overwhelm the conversation.
    
    One tip to keep yourself calm and grounded during the interview is to focus on your breathing. Take slow, deep breaths to help regulate your emotions and provide a sense of calmness. Additionally, practice your answer to the question beforehand so that you can feel more confident and prepared when answering the question. Remember, it's okay to have failed in the past as long as you can show that you learned from the experience and grew as a result.`, // String - paragraph explaining how to improve, etc...

  audioAnalysis: `In this interview, you've displayed an angry voice expression for the majority of the time. Your tone was sharp and intense, with a hint of frustration evident in your delivery. The audio conveyed a sense of aggression and impatience, which could potentially create a hostile atmosphere and hinder effective communication. To improve the audio, it is essential to work on managing your emotions and maintaining a more composed and neutral tone throughout the interview. This can be achieved by practicing deep breathing techniques and consciously monitoring your voice modulation.
  
    Additionally, it is crucial to focus on active listening and allowing the other person to speak without interruption. By actively engaging in a two-way conversation and practicing empathy, you can create a more respectful and productive environment. It's important to remember that effective communication involves not only expressing your thoughts and concerns but also actively listening to others' perspectives and responding in a respectful manner. Taking the time to pause, reflect, and respond thoughtfully can help diffuse anger and promote a more constructive dialogue.
    
    Furthermore, incorporating positive language and choosing your words carefully can make a significant difference in the tone of the interview. Using more neutral and objective language instead of personal attacks or accusatory statements can help create a more professional and respectful atmosphere. Additionally, focusing on the main points and maintaining a clear and concise communication style can prevent misunderstandings and unnecessary conflict. Practice active communication techniques, such as paraphrasing and clarifying information, to ensure effective comprehension and minimize any potential anger-inducing miscommunication.
    
    By implementing these strategies and maintaining a composed and respectful demeanor, you can improve the audio of the interview and promote a more constructive and harmonious conversation.`, // String - paragraph explaining how to improve, etc...

  contentOverall: "Detailed1", // String - overall description of content like "detailed"
  contentScore: 88, // String - overall score of content like 88 out of 100
  contentAnalysis: `In this interview, the content was excellent and very detailed. You demonstrated an impressive depth of knowledge and provided comprehensive responses to the questions asked. Your ability to articulate complex concepts clearly and concisely was commendable, making it easy for the audience to follow along. The content was well-structured, with a logical flow that allowed for a thorough exploration of the topic at hand. Your expertise and attention to detail were evident throughout, which greatly enhanced the overall quality of the interview.
  
    To further improve the interview's content, one suggestion would be to incorporate more real-world examples or case studies. While your explanations were thorough, the addition of specific instances or practical applications can help illustrate your points and make them more relatable to the audience. By providing tangible examples, you can enhance the understanding and engagement of listeners, as well as demonstrate the practicality and relevance of your expertise.
    
    Another area of improvement could be to incorporate a more interactive approach. Although the content was detailed, there were limited opportunities for engagement with the interviewer or the audience. Consider integrating questions or prompts that encourage active participation, such as asking for opinions or experiences related to the topic. This will not only create a more dynamic and engaging conversation but also foster a sense of collaboration and inclusivity.
    
    Furthermore, it is essential to strike a balance between technical depth and accessibility. While it is admirable to provide detailed information, ensure that it is presented in a manner that can be easily understood by a broader audience. Avoid excessive jargon or technical terms without providing sufficient context or explanations. Strive to maintain clarity and simplicity in your explanations, allowing listeners with varying levels of familiarity with the subject matter to grasp the key points effectively.
    
    By incorporating these suggestions, such as utilizing real-world examples, promoting interactivity, and maintaining accessibility, you can further enhance the already excellent content of the interview. These improvements will not only engage and educate the audience but also solidify your position as an expert in the field.`, // String - paragraph explaining how to improve, etc...
};
