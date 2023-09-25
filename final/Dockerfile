FROM python:3.9-slim

ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

WORKDIR .

# COPY requirements.txt .
# RUN pip install -r requirements.txt

COPY /src .

RUN ls -a

EXPOSE 8080

CMD ["python", "main.py"]
