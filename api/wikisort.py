import wikipedia
from gensim.summarization import keywords
from gensim.summarization import summarize
from bs4 import BeautifulSoup
import requests
import Levenshtein
import json
import flask
from datetime import datetime

def wordRelevance(topic):

    page = wikipedia.page(topic,auto_suggest=True)

    try:
        page = wikipedia.page(topic)
    except wikipedia.exceptions.PageError:
        return json.dumps(["Try " , "a more", "specific", "topic"])
    content = page.content
    
    pagesummary = wikipedia.summary(topic, sentences=1).lower().split(" ")
    links = page.links
    temp = []

    real_links = {}

    for each in links:
        output_link = each
        if '(' in each:
            output_link = each[:each.index('(')]
            output_link = output_link.replace(" ","")
        
        temp.append(output_link.lower())
        real_links[output_link.lower()] = each

    links = temp

    output = {}
    checker = []
    listofscores = []
    threshold = 1
    while (len(listofscores) < 5):
        for each2 in links:
            for each in pagesummary:
                if  each != topic.lower() and each2 != topic.lower():
                    stringsimilarity = Levenshtein.ratio(each,each2)

                    if stringsimilarity >= threshold:
                        if each2 not in checker:
                            checker += [each2]
                            listofscores += [[each2, stringsimilarity]]
        threshold = threshold - 0.1

    listofscores.sort(key=lambda x: x[1], reverse=True)
    result = []
    for each in listofscores[:4]:
        result += [each[0]]
    return result
    

def summaries(topics):
    print(topics)
    topics = topics.split("+")
    summaries = []
    for topic in topics:
        try:
            page = wikipedia.page(topic)
            content = page.content
            summaries.append(summarize(content, word_count = 200))
        except wikipedia.exceptions.PageError:
            summaries.append("Sorry, this page was not found on wikipedia")

    
    return summaries


	