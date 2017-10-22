import wikipedia
from gensim.summarization import keywords
from gensim.summarization import summarize
import wptools as wp


def wordRelevance(topic):
	
    page = wikipedia.page(topic,auto_suggest=True)
    content = page.content
    summary = page.summary

#('skeptical', array([ 0.0271428]))
    links = page.links

    for i in range(0,len(links)):
        links[i] = links[i].lower()

    #print links
   
    keys = keywords(content)


    #print summarize(content, word_count=100,ratio=0.1)

    sLinks = []

    #print keys
    #print 'Links:'
    #print links
    for link in links:
        if link in keys:
            sLinks.append(link)

    #print sLinks
	
    return summarize(content, word_count=100,ratio=0.1)

 
	# print(summarize(content, word_count = 100))