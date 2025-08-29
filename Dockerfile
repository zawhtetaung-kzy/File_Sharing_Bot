# Base image ကို Python 3.10.8-slim-bullseye အနေနဲ့ သတ်မှတ်ခြင်း
FROM python:3.10.8-slim-bullseye

# Server ရဲ့ Package တွေကို update လုပ်ပြီး git ကို install လုပ်ခြင်း
RUN apt-get update && apt-get upgrade -y

# Bot ရဲ့ လိုအပ်တဲ့ library တွေကို install လုပ်ရန် requirements.txt ကို copy ကူးခြင်း
COPY requirements.txt /requirements.txt
RUN pip3 install -U pip && pip3 install -U -r /requirements.txt

# Bot အတွက် folder တစ်ခုဖန်တီးပြီး working directory အဖြစ်သတ်မှတ်ခြင်း
RUN mkdir /File_Sharing_Bot
WORKDIR /File_Sharing_Bot

# Project files တွေအားလုံးကို Docker image ထဲကို copy ကူးခြင်း
COPY . /File_Sharing_Bot

# Bot ကို စတင် run ရန် command ကိုသတ်မှတ်ခြင်း
CMD ["python", "main.py"]
