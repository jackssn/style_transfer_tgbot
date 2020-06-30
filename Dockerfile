FROM python:3.7

ENV API_TOKEN="<YOUR_TOKEN_HERE>"

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/jackssn/style_transfer_tgbot.git

WORKDIR style_transfer_tgbot

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot_pooling.py"]