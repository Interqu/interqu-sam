FROM public.ecr.aws/lambda/python:3.10

COPY app.py requirements.txt ./
COPY pretrain.t7 /opt/ml/pretrain.t7
COPY haarcascade_frontalface_default.xml /opt/ml/haarcascade_frontalface_default.xml

RUN python3.10 -m pip install -r requirements.txt -t .




CMD ["app.lambda_handler"]
