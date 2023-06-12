import torch
import torchvision
import base64
import json
import numpy as np

import torch.nn as nn
import torch.nn.functional as F

from PIL import Image
from io import BytesIO

import cv2
from collections import defaultdict
import os

import boto3


s3_client = boto3.client("s3")

transform = torchvision.transforms.Compose([
    torchvision.transforms.TenCrop(44),
    torchvision.transforms.Lambda(lambda crops: torch.stack([torchvision.transforms.ToTensor()(crop) for crop in crops])),
])

VGG19CFG = [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M']

class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        self.features = self._make_layers(VGG19CFG)
        self.classifier = nn.Linear(512, 7)

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = F.dropout(out, p=0.5, training=self.training)
        out = self.classifier(out)
        return out

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                           nn.BatchNorm2d(x),
                           nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)


classes = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']




model_file = '/opt/ml/pretrain.t7'
face_model = '/opt/ml/haarcascade_frontalface_default.xml'
net = VGG()

if torch.cuda.is_available():
    checkpoint = torch.load(model_file)
    net.load_state_dict(checkpoint['net'])
    device = torch.device("cuda")
else:
    checkpoint = torch.load(model_file, map_location = torch.device("cpu"))
    net.load_state_dict(checkpoint['net'])
    device = torch.device("cpu")

net.to(device)




def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def lambda_handler(event, context):
    face_cascade = cv2.CascadeClassifier(face_model)

    video = event["queryStringParameters"]["file_name"]

    if not video:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "no file name was provided",
                }
            ),
        }


    s3_client.download_file("interqu-video", video, "/tmp/video.mp4")
    
    
    cap = cv2.VideoCapture("/tmp/video.mp4")
    success, image = cap.read()
    count = 0
    out = defaultdict(lambda:0, {})
    timeline = []
    total_score = 0

    while success:
        success, raw = cap.read()
        if count % 30 == 0:

            gray = rgb2gray(raw)
            gray = np.array(gray, dtype = "uint8")
            faces = face_cascade.detectMultiScale(gray, 1.1, 10)
            # faces = 0
            # Face detected, we use this frame
            if len(faces) > 0:
                faces = faces[0] # We want to take only 1 face

                gray = gray[faces[1]:faces[1] + faces[3], faces[0]:faces[0]+faces[2]]
                gray = cv2.resize(gray, dsize = (48,48), interpolation = cv2.INTER_LINEAR)

                img = gray[:, :, np.newaxis]

                img = np.concatenate((img, img, img), axis=2)
                img = Image.fromarray(img)
                inputs = transform(img)

                with torch.no_grad():   
                    net.eval()

                    ncrops, c, h, w = np.shape(inputs)

                    inputs = inputs.view(-1, c, h, w)
                    inputs = inputs.to(device)
                    outputs = net(inputs)

                    outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops
                    score = F.softmax(outputs_avg, dim = -1)

                    _, predicted = torch.max(outputs_avg.data, 0)

                out[classes[int(predicted.cpu().numpy())]] +=1
                timeline.append(classes[int(predicted.cpu().numpy())])
                count += 1
        else: 
            count += 1

    # Scoring
    scores = {'Angry': 0, 'Disgust':0.1, 'Fear' : 0.2, 'Happy': 1, 'Sad':0.3, 'Surprise':0.5, 'Neutral':0.5}

    for item in out:
        total_score += scores[item] * out[item]



    return_obj = {"Score" : total_score, "Timeline": timeline}

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "output": return_obj,
            }
        )
    }
