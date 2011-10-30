import feedparser

def parse(url):
    feed = feedparser.parse(url)
    feed_list = []
    #TODO Add in template uls, format date, load image item['summary']
    for item in feed['items']:
        feed_list.append(item)
    return feed_list
