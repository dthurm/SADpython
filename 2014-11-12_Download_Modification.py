# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 16:43:23 2014

@author: Daniel Thurmberger, Thimo Marchl
"""


from TwitterAPI import TwitterAPI
from cred import *
import pyodbc
import time
from textblob import TextBlob
import sys
import nltk
import string
from scipy.stats.stats import pearsonr

def downloadTweets():
    """consumer_key='o4Wlvr4h9pNZKeLgQ7rB54FMU'
    consumer_secret='jBlPvAzZWqKxo8rknPZFkpkkVuvStcstrZyeme28qsIInU3o7n'
    access_token='2873979395-rtE2xVUcF5qjPd3EOAd1cfkxbcyjPhsFoyum3oh'
    access_token_secret='ymWnOfafcokcFpx1cKGaSfbnUrmTOt5CBNs1kGapwNLP2'"""
    
    
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
        
    r=api.request('statuses/filter', {'track':'facebook'})
    for item in r:
        #print item
        if (item['lang']=="en"):
            #print item['id']
            #print item['lang']
            #writeJson(item)
            #calcSA
            #calcSATB
            try:
                insertInto(item,getSentimentScore(str(item["text"])),getSentimentScoreTB(str(item["text"])))
                print "#############################################################################"
            except:
                z = sys.exc_info()
                print z

def getAggregates():
    sqlDay = "select avg(score) from tweets where created_at > date_add(now(), INTERVAL -1 DAY)"
    sqlWeek = "select avg(score) from tweets where created_at > date_add(now(), INTERVAL -1 WEEK)"
    sqlMonth = "select avg(score) from tweets where created_at > date_add(now(), INTERVAL -1 MONTH)"
    sqlYear = "select avg(score) from tweets where created_at > date_add(now(), INTERVAL -1 YEAR)"

    result = dict()    
    
    cursor.execute(sqlDay)
    result["day"] = cursor.fetchall()[0][0]
    
    cursor.execute(sqlWeek)
    result["week"] = cursor.fetchall()[0][0]
    
    cursor.execute(sqlMonth)
    result["month"] = cursor.fetchall()[0][0]

    cursor.execute(sqlYear)
    result["year"] = cursor.fetchall()[0] [0]
    
    return result

def getSentimentScoreTB(tweet):
    blob = TextBlob(tweet)
    score = blob.sentiment.polarity
    print "TextBlob score calculated successfully"
    return score

def exportToCSV(start, end, name):
    sql = "select created_at, score, scoreTB from tweets where created_at > '" + start + "' and created_at < '" + end + "'"
    
    cursor.execute(sql)
    rows = cursor.fetchall()

    f = open(name + ".csv", 'wb')    
    
    for row in rows:
        f.write(str(row[0]) + ";" + str(row[1]) + ";" + str(row[2]) +"\n")
        
    f.close()
    print "File: " + name + ".csv was written successfully!"
    
    
def insertInto(x, score, scoreTB):
    
    try:
        tweet_id = str(x['id'])
        user_name = str(x['user']['screen_name'])
        created_at = x['created_at']
        date = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        date = time.strftime('%Y-%m-%d %H:%M:%S', date)
        #print date
        text = str(x['text']).replace("'","''")
        score = str(score)
        scoreTB = str(scoreTB)
    
        cursor.execute("INSERT INTO tweets (tweet_id, user_name, created_at, text, score, scoreTB) VALUES (" + "'" + tweet_id + "','" + user_name + "','" + date + "','" + text + "'" + "," + score + "," + scoreTB + ")")
        cursor.commit()
        print "Tweet inserted successfully"
    except:
        z = sys.exc_info()
        print z


def get_sentiment_incrementers():
    f = open("Incrementers.txt","r")
    increment_dict = dict()
    for line in f:
        l = line.split("\t")
        increment_dict[l[0]] = float(l[1])
    return increment_dict
    
def get_sentiment_decrementers():
    f = open("Decrementers.txt","r")
    decrement_dict = dict()
    for line in f:
        l = line.split("\t")
        decrement_dict[l[0]] = float(l[1])
    return decrement_dict    
    
def get_sentiment_dictionary():
    f = open("AFINN-111.txt","r")
    senti_dict = dict()
    for line in f:
        l = line.split("\t")
        senti_dict[l[0]] = float(l[1])
    return senti_dict
    
def getSentimentScore(tweet_text):
    
    words = nltk.word_tokenize(tweet_text.translate(None, string.punctuation))
    
    senti_score = 0.0
    word_before = ""
    
    for word in words:      
        if increment_dict.has_key(word_before) or decrement_dict.has_key(word_before):
            if senti_dict.has_key(word):
                if increment_dict.has_key(word_before):
                    senti_score = senti_score + (senti_dict[word] * increment_dict[word_before])
                elif decrement_dict.has_key(word_before):
                    senti_score = senti_score + (senti_dict[word] * decrement_dict[word_before])
        elif senti_dict.has_key(word):
            senti_score = senti_score + senti_dict[word]
                    
        word_before = word

    score = senti_score/len(words)
    print "Sentiment score calculated successfully"
    return score
    
def getCorr():
    sql = "select score, scoretb from tweets"
    x = []
    y = []

    cursor.execute(sql)
    rows = cursor.fetchall()
    
    for row in rows:
        x.append(row[0])
        y.append(row[1])
        
    return pearsonr(x,y)
    
        
#Start of main program

"""server="pma.iwiserver.com"
port="3306"
db="group1"
uid="uni06"
pw="daniel"""

conn = pyodbc.connect("DRIVER={MySQL ODBC 5.3 Unicode Driver}; SERVER="+server+"; PORT="+port+"; DATABASE="+db+"; UID="+uid+"; PASSWORD="+pw+";")
cursor = conn.cursor()

selection = input("Enter [1] for downloading tweets, [2] for getting statistics, [3] for export to csv, [4] for correlation between sentiment scores: ")

if selection == 1:
    decrement_dict = get_sentiment_decrementers()
    increment_dict = get_sentiment_incrementers()
    senti_dict = get_sentiment_dictionary()
    downloadTweets()
elif selection == 2:
    results = getAggregates()
    
    print "day-avg: " + str(results["day"])
    print "week-avg: " + str(results["week"])
    print "month-avg: " + str(results["month"])
    print "year-avg: " + str(results["year"])
elif selection == 3:
    start = raw_input("Set start date (YYYY-MM-DD): ")
    end = raw_input("Set end date (YYYY-MM-DD): ")
    name = raw_input("Set filename: ")
    exportToCSV(start,end,name)
elif selection == 4:
    print "Pearson correlation: "+ str(getCorr()[0])
    print "Two-tailed p-value: "+ str(getCorr()[1])
else:
    print "Wrong selection!"
    
#calcExisting()

#getAggregates()
#exportTweetsToCSV("2014-11-26 16:00:00","2014-11-26 17:00:00")