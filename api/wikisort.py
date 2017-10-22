import wikipedia
from gensim.summarization import keywords
from gensim.summarization import summarize
from bs4 import BeautifulSoup
import requests
import Levenshtein
import json
from datetime import datetime

def wordRelevance(topic):

    page = wikipedia.page(topic,auto_suggest=True)

    startTime= datetime.now()

    try:
        page = wikipedia.page(topic)
    except wikipedia.exceptions.PageError:
        return json.dumps(["Try " , "a more", "specific", "topic"])
    content = page.content
    summary = page.summary
    pagesummary = wikipedia.summary(topic, sentences=1).lower().split(" ")

    print("1 {}".format(datetime.now()-startTime))
    startTime= datetime.now()

    the_keywords = keywords(content, scores = True)

    print("2 {}".format(datetime.now()-startTime))
    startTime= datetime.now()

    not_topic= []
    for each in the_keywords:
        if(Levenshtein.ratio(each[0], topic.lower()) < .77):
            not_topic.append(each)

    the_keywords = not_topic

#('skeptical', array([ 0.0271428]))
    links = page.links

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


    print("3 {}".format(datetime.now()-startTime))
    startTime= datetime.now()

    links = temp

    output = {}

    wnl = WordNetLemmatizer()
    listofscores = []
    threshold = 1
    while (len(listofscores) < 5):
        for each2 in links:
            for each in pagesummary:
                if  each != topic.lower() and each2 != topic.lower():
                    stringsimilarity = Levenshtein.ratio(each,each2)

                    if stringsimilarity >= threshold:
                        if [each2,stringsimilarity] not in listofscores:
                            listofscores += [[each2, stringsimilarity]]
        threshold = threshold - 0.05


    result = []
    ultimatelistofscores = listofscores[:4]
    for each in listofscores[:4]:
        result.append(each[0])
    output['0.99'] = result

    print("4 {}".format(datetime.now()-startTime))
    startTime= datetime.now()

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




    storing_dic = {}
    count = 0;

    for each in testing_links:
        storing_dic[each] = link_power(each) * (2 ** (-count) * .5 + 1) * output[each] #weights it according to relevance
        count += 1

    sorted_dic = list(storing_dic.items())


    sorted_dic.sort(key=lambda x: x[1], reverse=True)

    titles = []
    for each in sorted_dic[:4]:
        titles.append(each[0])


    print("total time {}".format(datetime.now()-startTime))
    startTime= datetime.now()


    summaries("+".join(titles))

    print("summary time {}".format(datetime.now()-startTime))

    return json.dumps(titles)



    #print links

    keys = keywords(content)
def link_power(topic):
    headers = {'user-agent': "sdhacks-cyficowley@gmail.com"}
    url = "https://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle={}&bllimit=5000&format=xml".format(topic)
    totalLength = 0
    for i in range(2):
        html = requests.get(url, headers= headers).content
        soup = BeautifulSoup(html, "lxml")
        length = len(soup.findAll('bl'))
        totalLength += length
        if not length == 500:
            break
        url = "https://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle={}&bllimit=500&format=xml&blcontinue={}".format(topic, soup.find('continue')["blcontinue"])

    return totalLength

    #print summarize(content, word_count=100,ratio=0.1)

    sLinks = []

    #print keys
    #print 'Links:'
    #print links
    for link in links:
        if link in keys:
            sLinks.append(link)
def summaries(topics):
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

    return summarize(content, word_count=100,ratio=0.1)
    return json.dumps(summaries)


	# print(summarize(content, word_count = 100))
