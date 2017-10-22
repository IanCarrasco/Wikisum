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
    startTime= datetime.now()
    page = ""

    topic = topic.lower()

    try:
        page = wikipedia.page(topic, auto_suggest=True)
    except wikipedia.exceptions.PageError:
        return json.dumps(["Try " , "a more", "specific", "topic"])

    content = page.content
    pagesummary = content[:content.index('.')]

    try:
        pagesummary = pagesummary[:pagesummary.index('(')] + pagesummary[pagesummary.index(')') + 1:]
    except ValueError:
        pass

    pagesummary = pagesummary.split()

    print(pagesummary)

    links = page.links

    the_keywords = keywords(content[:int(len(content)/2)], scores = True, ratio= .05)


    delta = 0
    for i in range(len(the_keywords)):
        if(the_keywords[i + delta][0] == topic):
            the_keywords.pop(i)
            delta -= 1

    for i in range(0,len(links)):
        links[i] = links[i].lower()

    temp = []

    real_links = {}

    for each in links:
        output_link = each
        if '(' in each:
            output_link = each[:each.index('(')]
        # if(Levenshtein.ratio(each.lower(), topic.lower()) < .77):
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
                if  each not in topic and each2 not in topic:
                    stringsimilarity = Levenshtein.ratio(each,each2)
                    if stringsimilarity >= threshold:
                        if each2 not in checker:
                            checker += [each2]
                            listofscores += [[each2, stringsimilarity]]
        threshold = threshold - 0.1

    listofscores.sort(key=lambda x: x[1], reverse=True)

    result = []
    ultimatelistofscores = listofscores[:4]
    for each in listofscores[:4]:
        result.append(each[0])
    output['0.99'] = result


    for each in the_keywords:
        for each2 in links:
            if each[0] in each2.split(" "):
                if str(each[1][0]) not in output:
                    output[str(each[1][0])] = []
                output[str(each[1][0])].append(each2)

    top_five = {} #top 5 best matches


    count = 0
    for key, value in output.items():
        if(count < 5):
            real_links_array = []
            for each in value:
                if(Levenshtein.ratio(real_links[each].replace(" ", "_"), topic) < .8):
                    real_links_array.append(real_links[each].replace(" ", "_"))
            top_five[key] = real_links_array
        else:
            break
        count += 1


    endrank = {i : "" for i in range(4)}



    testing_links = []


    allowed_links = [3,2,1,1,1] # gets top 8 links hopefully
    count = 0
    for key, value in top_five.items():
        value = sorted(value , key = len)

        if(len(value) < allowed_links[count]):
            testing_links += value
        else:
            testing_links +=  value[0:allowed_links[count]]

        if(count < 4 and len(value) < allowed_links[count]):
            allowed_links[count + 1] += allowed_links[count] - len(value)
        count += 1


    output = {i : 1 for i in testing_links}

    #optimized


    storing_dic = {}
    count = 0;

    for each in testing_links:
        storing_dic[each] = (2 ** (-count) * .5 + 1) * output[each] #weights it according to relevance
        count += 1



    sorted_dic = list(storing_dic.items())


    sorted_dic.sort(key=lambda x: x[1], reverse=True)

    titles = []
    for each in sorted_dic[:4]:
        titles.append(str(each[0]))

    print(datetime.now() - startTime)


    return titles
    #print links



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

    #print sLinks
    return summaries


	# print(summarize(content, word_count = 100))
