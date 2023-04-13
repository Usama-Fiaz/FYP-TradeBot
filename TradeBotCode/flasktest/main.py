import csv
import json
import nltk
from flask import Flask, jsonify

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# nltk.download('vader_lexicon')

from collections import namedtuple
from json import JSONEncoder
from flask import Flask,request

from flask_cors import CORS

from transformers import AutoTokenizer, AutoModelForSequenceClassification


from NewsFetchScript import Fetch_News
from TweetsFetchScript import Fetch_Tweets
# from MetaTrader import makingOrder
# from MetaTrader import getTradeHistory
# check oint

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")




import numpy as np

app = Flask(__name__)

CORS(app)


@app.route("/makeorder")
def post_makeorder_request():
    try:
        volume = request.args.get('volume')
        volume = float(volume)
    except ValueError:
        # Handle the exception here
        return (json.dumps("Vol value manipulated"))


    trademode = request.args.get('trademode')
    symbol = request.args.get('symbol')

    print("vol = ", volume,type(volume), "\ntrade mode",trademode, "Symbol = ", symbol)

    if volume and trademode and symbol:
        result = makingOrder(volume,trademode,symbol)
        if result:
            return (json.dumps("order placed"))
        else:
            return (json.dumps("some error occurred.."))

    else:
        return (json.dumps("Required vol and trade mode"))


@app.route("/gettradinghistory")
def get_tradeorder_request():
    return (json.dumps(getTradeHistory()))


@app.route("/getnews")
def get_news():
    About = request.args.get('About')
    newsdata = Fetch_News(About)

    print("Recieved the Get Request for = ",About)
    return (json.dumps(newsdata))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

print("started")


def customStudentDecoder(InputDict):
    return namedtuple('X', InputDict.keys())(*InputDict.values())


import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB Atlas

client = pymongo.MongoClient("mongodb+srv://usama-fiaz:usama2001fiaz@cluster0.at3lai3.mongodb.net/?retryWrites=true&w=majority")


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

@app.route("/sentimentalanalysis/topic")
def sentimental_analysis_of_newstopic():
    topic = request.args.get('topic')

    print("Fetching News for "+topic)

    query = {"topic": topic}
    projection = {"_id": 0}
    db = client["News_Database"]
    collection = db[topic+"_News"]
    newsdata = list(collection.find(query, projection).sort('timestamp', -1).limit(100))

    if newsdata == []: # If News are not present in the database, then Fetch them
        fetch_and_save_News_data(topic)
        newsdata = list(collection.find(query, projection).sort('timestamp', -1))

    return json.dumps(newsdata, cls=CustomEncoder)

def fetch_and_save_News_data(topic):
    print("Automatic API Call to fetch news for "+topic)

    newsdata = Fetch_News(topic)
    db = client["News_Database"]
    collection = db[topic+"_News"]

    for newsitem in newsdata:
        inputs = tokenizer(newsitem["title"], return_tensors="pt")
        outputs = model(**inputs)[0]

        labels = {0: 'positive', 1: 'negative', 2: 'neutral'}

        answer_label = labels[np.argmax(outputs.detach().numpy())]
        newsitem["Prediction"] = answer_label

        newsitem["topic"] = topic
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        newsitem["timestamp"] = formatted_time
        collection.insert_one(newsitem)


import pandas as pd

@app.route('/getChartData')
def get_data_from_csv():
    with open('eurusd.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            date = datetime.strptime(row['time'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d')
            data.append({
                'x': date,
                'y': [float(row['open']), float(row['high']), float(row['low']), float(row['close'])]
            })
        return data



@app.route("/sentimentalanalysis/tweetstopic")
def sentimental_analysis_of_tweetstopic():
    topic = request.args.get('topic')

    print("Fetching Tweets for "+topic)
    query = {"topic": topic}
    projection = {"_id": 0}
    db = client["Tweets_Database"]
    collection = db[topic+"_Tweets"]
    tweetsdata = list(collection.find(query, projection).sort('date', -1).limit(100))

    if tweetsdata == []: # If tweets are not present in the database, then Fetch them
        fetch_and_save_Tweets_data(topic)
        tweetsdata = list(collection.find(query, projection).sort('date', -1))

    return json.dumps(tweetsdata, cls=CustomEncoder)

def fetch_and_save_Tweets_data(topic):
    print("Automatic API Call to fetch Tweets for "+topic)

    tweetsdata = Fetch_Tweets(topic)
    db = client["Tweets_Database"]
    collection = db[topic+"_Tweets"]

    for tweetitem in tweetsdata:
        inputs = tokenizer(tweetitem["tweet"], return_tensors="pt")
        outputs = model(**inputs)[0]

        labels = {0: 'positive', 1: 'negative', 2: 'neutral'}

        answer_label = labels[np.argmax(outputs.detach().numpy())]
        tweetitem["Prediction"] = answer_label
        tweetitem["topic"] = topic
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        tweetitem["timestamp"] = formatted_time
        collection.insert_one(tweetitem)

# scheduler = BackgroundScheduler()

# # Automatically News Data Fetching and Saving to MongoDB Atlas

# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=1, args=["EUR/USD"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=1, args=["GBP/USD"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=1, args=["USD/JPY"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=1, args=["AUD/USD"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=2, args=["EUR/GBP"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=2, args=["USD/CAD"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=2, args=["USD/CHF"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=2, args=["NZD/CHF"])
# scheduler.add_job(fetch_and_save_News_data, 'interval', minutes=2, args=["Forex"])

# # Automatically Tweets Data Fetching and Saving to MongoDB

# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["EUR/USD"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["GBP/USD"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["USD/JPY"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["AUD/USD"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["EUR/GBP"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["USD/CAD"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["USD/CHF"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["NZD/CHF"])
# scheduler.add_job(fetch_and_save_Tweets_data, 'interval', minutes=11, args=["Forex"])

# scheduler.start()

@app.route("/newssentimentalanalysis")
def sentimental_analysis():
    # Transform input tokens
    sentences = ["EUR/USD regains the smile and retargets the parity level",
                 "EUR/USD Short-term Technical Outlook: Euro Post-CPI Plunge to Parity - DailyFX",
                 "Euro Forecast: EUR/USD Soars as Dollar Loses Sparkle Ahead of US Inflation Report - DailyFX",
                 "EUR/USD: Failure to breach 1.02 after US CPI to disappoint bulls“ TDS - FXStreet",
                 "EUR/USD: Devaluation risks for the euro as long as energy crisis is not over“ Commerzbank - FXStreet",
                 "BUZZ-COMMENT-US inflation puts EUR/USD's December 2002 low in focus - Nasdaq",
                 "EUR/USD remains under pressure after short-lived rebound - FXStreet",
                 "Due to #CPI report the opposite effect of pure negative energy didn't work today, Sep 13. However, all time frames and weaknesses worked perfectly.",
                 "EUR/USD King dollar is back",
                 "EUR/USD Short-term Technical Outlook: Euro Post-CPI Plunge to Parity",
                 "been accumulating EUR/USD its time to fly. up only.",
                 "dump all your dog coin for EUR/USD",
                 "nobody on ct is talking about EUR/USD am i early? maybe will i get left with a bag that doesnt move? fairly likely ngmi",
                 "bcz of this news the good projects like EUR/USD will start to pump",
                 "bullish on . time for it to breakout soon. was always bullish on and EUR/USD and will always be."
                 "my EUR/USD finally breaking out again still standing by my commitment to getting an antshares tattoo when it hits"]

    # inputs = tokenizer("Hello world!", return_tensors="pt")

    inputs = tokenizer(sentences, return_tensors="pt", padding=True)
    outputs = model(**inputs)[0]

    # Model apply
    # outputs = model(**inputs)
    # print(outputs)

    # positive, negative or neutral.

    labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
    answers = []
    for idx, sent in enumerate(sentences):
        answers.append(sent+'---'+labels[np.argmax(outputs.detach().numpy()[idx])])
        print(sent, '----', labels[np.argmax(outputs.detach().numpy()[idx])])
    return answers



if __name__  == '__main__':
    app.run(debug=True)