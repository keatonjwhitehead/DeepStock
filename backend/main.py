from flask import Flask
from flask_cors import CORS
from alpha_vantage.timeseries import TimeSeries
from flask import request
from flask_pymongo import pymongo
from pymongo import MongoClient
import yfinance as yf
from datetime import tzinfo, timedelta, datetime
import json
from bson import json_util

#from twitter import TwitterClient
from google.oauth2 import service_account
from googleapiclient import discovery
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

CONNECTION_STRING = "mongodb://deep-stock-cu:deep2020stock@deep-stock-cluster-shard-00-00-bwk5a.gcp.mongodb.net:27017,deep-stock-cluster-shard-00-01-bwk5a.gcp.mongodb.net:27017,deep-stock-cluster-shard-00-02-bwk5a.gcp.mongodb.net:27017/test?ssl=true&replicaSet=deep-stock-cluster-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('deep-stock')
collection = db['companies']


CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/message')
def get_message():
    return 'Hello Stonks'

# adds historicaldata to ticker and retrieves all historical data from db
@app.route("/<string:company>/historicaldata", methods=['PUT' , 'GET'])
def addhist(company):
    if request.method == 'PUT': ## NEDS UPDATING
        new_hist = request.get_json()
        collection.update({"ticker" : company}, {'$push': {'historical': new_hist}})
        return("Historical data added to: " + company)
    if request.method == 'GET':
        obj = collection.find_one({"ticker": company})
        #print(obj['historical'][:10])
        #return json.dumps(obj['historical'], indent=4, sort_keys=True, default=str)
        return json.dumps(obj['historical'], default=json_util.default)


# adds new company with it's current metadata
@app.route("/company", methods=['POST'])
def addcompany():
    companyObj = request.get_json()
    collection.insert_one(companyObj)
    addMetadata(companyObj['ticker'])
    addhist2year(companyObj['ticker'])

@app.route("/<string:company>/metadata", methods=['GET'])
def getMetadata(company):
    obj = collection.find_one({'ticker' : company})
    return obj['metadata']


@app.route("/<string:company>/two_week_hist", methods=['GET']) # MAYBE CHANGE RETURN FROM LIST TO SOMETHING ELSE
def get_2weekhist(company):
    comp = yf.Ticker(company)
    hist = comp.history(period="14d")
    hist2 = hist.to_dict('index')
    pred = []
    for i in hist2:
        tmp = {'date' : i}
        tmp.update(hist2[i])
        pred.append(tmp)
    return json.dumps(pred, default=json_util.default)

# Adds the metadata to database base on ticker
def addMetadata(company):
    comp = yf.Ticker(company)
    jsonY = comp.info
    data = {}
    data = tryObj('shortName', jsonY, data)
    data = tryObj('logo_url', jsonY, data)
    data = tryObj('website', jsonY, data)
    data = tryObj('symbol', jsonY, data)
    data = tryObj('city', jsonY, data)
    data = tryObj('phone', jsonY, data)
    data = tryObj('industry', jsonY, data)
    data = tryObj('country', jsonY, data)
    data = tryObj('state', jsonY, data)
    data = tryObj('currency', jsonY, data)
    data = tryObj('longBusinessSummary', jsonY, data)
    data = tryObj('zip', jsonY, data)
    data = tryObj('sector', jsonY, data)
    data = tryObj('fullTimeEmployees', jsonY, data)
    data = tryObj('address1', jsonY, data)
    data = tryObj('longName', jsonY, data)
    collection.update({"ticker" : company}, {'$set': {'metadata': data}}) #for now test5 but change later

# route to add fundamentals with current timestamp in NY
@app.route("/<string:company>/fundamentals", methods=['PUT' , 'GET'])
def addfundamentals(company):
    if request.method == 'PUT':
        comp = yf.Ticker(company)
        jsonY = comp.info
        td = datetime.now()
        td = td - timedelta(hours=5)
        data = {'date' : td}
        data = tryObj('sharesShort', jsonY, data)
        data = (tryObj('trailingPE', jsonY, data))
        data = (tryObj('trailingEps', jsonY, data))
        data = (tryObj('enterpriseToRevenue', jsonY, data))
        data = (tryObj('fiftyDayAverage', jsonY, data))
        data = (tryObj('averageDailyVolume10Day', jsonY, data))
        data = (tryObj('bookValue', jsonY, data))
        data = (tryObj('volume', jsonY, data))
        data = (tryObj('SandP52WeekChange', jsonY, data))
        data = (tryObj('fiftyTwoWeekHigh', jsonY, data))
        data = (tryObj('netIncomeToCommon', jsonY, data))
        data = (tryObj('averageVolume10days', jsonY, data))
        data = (tryObj('regularMarketVolume', jsonY, data))
        data = (tryObj('earningsQuarterlyGrowth', jsonY, data))
        data = (tryObj('52WeekChange', jsonY, data))
        data = (tryObj('sharesShortPriorMonth', jsonY, data))
        data = (tryObj('heldPercentInsiders', jsonY, data))
        data = (tryObj('marketCap', jsonY, data))
        data = (tryObj('beta', jsonY, data))
        data = (tryObj('priceToSalesTrailing12Months', jsonY, data))
        data = (tryObj('shortRatio', jsonY, data))
        data = (tryObj('averageVolume', jsonY, data))
        data = (tryObj('shortPercentOfFloat', jsonY, data))
        data = (tryObj('fiftyTwoWeekLow', jsonY, data))
        data = (tryObj('forwardPE', jsonY, data))
        data = (tryObj('profitMargins', jsonY, data))
        data = (tryObj('heldPercentInstitutions', jsonY, data))
        data = (tryObj('forwardEps', jsonY, data))
        data = (tryObj('twoHundredDayAverage', jsonY, data))
        collection.update({"ticker" : company}, {'$push': {'fundamentals': data}})
        return "fundamentals added to: " +  company +  " for date: " + str(td)
    if request.method == 'GET':
        obj = collection.find_one({'ticker' : company})
        fun = obj['fundamentals']
        funSize = len(obj['fundamentals']) - 1
        return fun[funSize]

# def for trying to add object in fundamentals, as some don't exist in other tickers

def tryObj(name , jsonY, data):
    try:
        data.update({name : jsonY[name]})
        return data
    except:
        return data

def getOne(ticker, date):
    date2 = date - timedelta(hours=24)
    startdate = datetime.strptime(date,'%Y-%m-%d')
    enddate = datetime.strptime(date2 ,'%Y-%m-%d')
    obj = collection.find_one({"ticker": ticker})
    for i in obj['historical']:
        if i['date'] > startdate and i['date'] < enddate:
            return i

def getlist(ticker, days): # Make sure is days
    enddate = datetime.now()
    startdate = enddate - timedelta(hours=24*days)
    obj = collection.find_one({"ticker": ticker})
    hist = []
    for i in obj['historical']:
        if i['date'] > startdate and i['date'] < enddate:
            hist.append(i)
    return hist

def addhist2year(company):
  comp = yf.Ticker(company)
  hist = comp.history(period="24mo")
  hist2 = hist.to_dict('index')
  for i in hist2:
    tmp = {'date' : i}
    tmp.update(hist2[i])
    collection.update({"ticker" : company}, {'$push': {'historical': tmp}})
  return ("added")


'''
  Storing stock data api
  Gets json data from response body and stores it into database
'''

@app.route('/users/store_data', methods=['POST'])
def insert_document():
    req_data = request.get_json()

    collection.insert_one(req_data).inserted_id
    return ('', 204)


'''
  Diplaying stock data api
  Gets all the sotored data in the database and retruns a json file
'''


@app.route('/<string:company>/intraday', methods=['GET'])
def get_intraday(company):

    print("getting called")


    key = 'CYNCL6X4FUN4SE0K'

    ts = TimeSeries(key= key)

    intraday_data, data_info = ts.get_intraday(symbol=company, outputsize='compact', interval='5min')


    daily_data = {}
    days_list = []
    convert_daytime = 0
    day = 0

    # Convert string dates to datetime format and append to list
    for key, value in intraday_data.items():
        convert_daytime = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        days_list.append(convert_daytime.day)


    # Get latest day
    latest_day = max(days_list)

    # Add filtered data to new dictionary
    for key, value in intraday_data.items():
        convert_daytime = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        day = convert_daytime.day

        if day == latest_day:
            if key not in daily_data:
                daily_data[key] = []
            daily_data[key].append(value)

    return json.dumps(daily_data)

@app.route('/users/display_data')
def get_documents():

    documents = collection.find()

    response = []

    for doc in documents:
        doc['_id'] = str(doc['_id'])
        response.append(doc)

    return json.dumps(response)

"""
@app.route('/tweepy/<string:ticker>', methods=['GET'])
def get_tweepy(ticker):
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query = ticker, count = 500)

    # store in mongodb
    for tweet in tweets:
        # might need to write condition to make sure tweets with same unique ID aren't duplicated

        # get date from iso datetime string
        tweet_date = datetime.strptime(tweet['date'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")

        #check if there is already a date object for tweet_date
        tweet_array = collection.find_one({"ticker" : ticker })["tweets"]
        tweet_date_exists = any(x for x in tweet_array if x["date"] == tweet_date)

        # if date object doesn't exist yet, add it
        if not tweet_date_exists:
            collection.update({"ticker" : ticker}, {'$push': {'tweets': {'date':tweet_date, 'day_sentiment': 0, 'tweets':[]}}})

        # add tweet to tweets array
        collection.update({"ticker" : ticker, "tweets.date": tweet_date}, {'$push': {'tweets.$.tweets': tweet}} )

        # recalculate day sentiment avg for each tweet added
        day_object = next((x for x in tweet_array if x["date"] == tweet_date), None)

        if day_object is None:
            avg_day_sentiment = 0
            updated_avg_day_sentiment = tweet["scaled_sentiment"]
        else:
            avg_day_sentiment = day_object["day_sentiment"]
            updated_avg_day_sentiment = ((avg_day_sentiment * len(day_object["tweets"])) + tweet["scaled_sentiment"])/(len(day_object["tweets"]) + 1)


        # calculate new average
        print(updated_avg_day_sentiment)

        # update daily sentiment
        collection.update({"ticker" : ticker, "tweets.date": tweet_date}, {'$set': {'tweets.$.day_sentiment': updated_avg_day_sentiment}} )

    return json.dumps(tweets, 200)
"""
# this deletes all tweets in database for a specified company
@app.route('/cleartweets/<string:ticker>', methods=['GET'])
def clear_tweets(ticker):
    collection.update({"ticker" : ticker}, { "$set": {"tweets": []}})

    return "cleared tweets for " + ticker

# get last 7 days sentiment 
@app.route('/<string:company>/recentdays', methods=['GET'])
def get_recent_sentiment(company):
    tweets_array = collection.find_one({"ticker" : company})
    recent_sentiment = tweets_array["tweets"]

    def get_date_string(elem):
        return int("".join(elem['date'].split('-')))

    sorted_recent_sentiment = sorted(recent_sentiment, key = get_date_string, reverse = True)

    return json.dumps(sorted_recent_sentiment[:7])


@app.route("/<string:company>/tweet_sentiments", methods=['GET'])
def get_tweets(company):
    obj = collection.aggregate([
        {'$match': {'ticker': company}},
        {'$unwind': '$tweets'},
        {'$project': {'tweets.day_sentiment': 1, 'tweets.date': 1}}
    ])
    res = []
    for entry in obj:
        res.append(entry)
    #obj = collection.find_one({"ticker": company},{'tweets': {$elemMatch: {}}})
    return json.dumps(res, default=json_util.default)

@app.route('/<string:company>/make_prediction', methods=['GET'])
def make_pred(company):
    hist_data = get_2weekhist(company)
    hist_data = json.loads(hist_data)
    #this should be changed to just get the prev week, eventually
    twit_data = get_tweets(company)
    twit_data = json.loads(twit_data)
    clean_twit = []
    for twit in twit_data:
        clean_twit.append({
            'date': (datetime.timestamp(datetime.strptime(twit['tweets']['date'], "%Y-%m-%d")))/100,
            'sent': twit['tweets']['day_sentiment']
        })

    df_hist = pd.DataFrame(hist_data)
    df_hist['date'] = df_hist['date'].map(lambda x: x['$date']/100000)

    df_twit = pd.DataFrame(clean_twit)
    df = pd.merge(df_hist, df_twit, on=['date'], how='left')
    df['sent'] = df['sent'].fillna(0)
    df = df.sort_values('date')
    input_data = (df[['Open', 'High', 'Low', 'Close', 'sent']].values)
    
    T = 7
    D = input_data.shape[1]
    
    scaler = StandardScaler()
    scaler.fit(input_data[:T])
    input_data = scaler.transform(input_data)
    X = np.zeros((1, T, D))
    X[0, :, :] = input_data[:T]

    instances = ({'input_1':X[0].tolist()})

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    service = discovery.build('ml', 'v1', credentials=credentials)
    response = service.projects().predict(
       name= 'projects/{}/models/{}'.format('deep-stock-268818', company),
        body={'instances': instances}
    ).execute()
    if 'error' in response:
        raise RuntimeError(response['error'])
    return json.dumps(response['predictions'])


if os.getenv('environment') == 'dev':
    app.run(host='0.0.0.0')
elif __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
