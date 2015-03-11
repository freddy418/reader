import feedparser
import re
import datetime
import HTMLParser

from HTMLParser import HTMLParser
#from boilerpipe.extract import Extractor

urls = []
keywords = []
titles = ""
count = 0

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# get the list of all the URLs that we want
fi=open("urls.list","r")
for line in fi:
    urls.append(line.strip())
fi.close

# get the list of all the keywords that we want
fi=open("keywords.list","r")
for line in fi:
    keywords.append(line.strip())
fi.close

fo=open("articles.txt", "w")

for url in urls:
    #print url
    feed = feedparser.parse(url)
    for post in feed.entries:
        
        # duplicate title?
        if (titles.find(post.title) >= 0):                    
            continue

        # date filter
        try:
            if (post.published_parsed.tm_year == datetime.datetime.now().year and
                post.published_parsed.tm_mon == datetime.datetime.now().month and
                post.published_parsed.tm_mday >= datetime.datetime.now().day-1 and
                post.published_parsed.tm_hour > 5):
                pass
            else:
                continue
        except:
            pass

        # todo: content filter
        # TODO

        # grab the title
        link = post.link

        # NYTIMES filter, since full site contains infinite loops
        if (url.find('nytimes') >= 0):
            #print "editing " + link
            link = re.sub(r'www.nytimes.com', "mobile.nytimes.com", link)
            link = re.sub(r'bits.blogs.nytimes.com', "mobile.nytimes.com/blogs/bits", link)
            link = re.sub(r'dealbook.nytimes.com', "mobile.nytimes.com/blogs/dealbook", link)
            link = re.sub(r'pogue.nytimes.com', "mobile.nytimes.com/blogs/pogue", link)
            link = re.sub(r'pogue.blogs.nytimes.com', "mobile.nytimes.com/blogs/pogue", link)
            #print "result " + link

        link = "<a href=\"" + link + "\">" + post.title + "</a></p>"
        #print text.encode('ascii', 'ignore')
        #print "\n" + "Opening " + link + "\n"
        
	article = strip_tags(post.summary)

        # keyword search against article and print if successful
        for kw in keywords:
            if (kw.lower() in (post.title + "\n" + article).lower()):
                # simple duplicate filter
                titles += post.title + "\n"
                count+=1
                print str(count) + ". " + link.encode('ascii', 'ignore')
                print article.encode('ascii', 'ignore')+"</p>"
                break

fo.close

#print "\n** " + str(count) + " articles found **"
