# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:03:39 2014

@author: Daniel Thurmberger, Thimo Marchl
"""

import nltk
import string
#import codecs
#sys.setdefaultencoding('utf-8')


#stop_words = []


def get_sentiment_incrementers():
    f = open("Incrementers.txt","r")
    increment_dict = dict()
    for line in f:
        line.decode('utf-8')
        l = line.split("\t")
        increment_dict[l[0]] = int(l[1])
    return increment_dict
    

#print increment_dict

def get_sentiment_decrementers():
    f = open("Decrementers.txt","r")
    decrement_dict = dict()
    for line in f:
        l = line.split("\t")
        decrement_dict[l[0]] = int(l[1])
    return decrement_dict    
        

#print decrement_dict

def get_sentiment_dictionary():
    f = open("AFINN-111.txt","r")
    senti_dict = dict()
    for line in f:
        l = line.split("\t")
        senti_dict[l[0]] = int(l[1])
    return senti_dict


#print senti_dict

#Eingefügt um Wörter abzufangen, die keinen positiven oder negativen Einfluss auf die Bewertung haben
#def stopword_list():
#    f = open("StopWords.txt", "r")
#    stop_words = []
#
#    line = f.readline()
#    while line:
#        word = line.strip()
#        stop_words.append(word)
#        line = f.readline()
#    f.close()
#    return stop_words
    
    
def sentiment_score(tweet_text):
    
    words = nltk.word_tokenize(tweet_text.translate(None,string.punctuation))
    
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

    return senti_score/len(words)

#Start    
tweet_text = "The weather is not bad today."

decrement_dict = get_sentiment_decrementers()
increment_dict = get_sentiment_incrementers()
senti_dict = get_sentiment_dictionary()

print sentiment_score(tweet_text)

