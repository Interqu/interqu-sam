const { MongoClient } = require("mongodb");

//TODO change with system env vars
const mongoURI = process.env.MONGODB_URL;
const dbName = "interqu";
const collectionName = "interview_result_data";

const javaDataClass = "com.interqu.interviews.InterviewVideoData";

exports.lambda_handler = async (event, context) => {
  return saveInterviewData(
    event["details"],
    event["visualData"],
    event["audioData"],
    event["GPTDescription"]
  );
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
    return {
      statusCode: 200,
      body: {
        message: "Data has successfully saved to database.",
      },
    };
  } catch (e) {
    console.log(e);
    return {
      statusCode: 500,
      body: {
        message: e,
      },
    };
  }
}
