FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY handler.py ./
COPY model.joblib ./
COPY scaler.joblib ./

CMD ["handler.lambda_handler"]