FROM python:3.8.6-buster

COPY api /api
COPY le_package /le_package
COPY model_le.joblib /model_le.joblib
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
