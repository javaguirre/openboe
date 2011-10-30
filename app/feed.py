import feedparser

def parse(url):
    feed = feedparser.parse(url)
    feed_list = []
    #TODO Add in template uls, format date, load image item['summary']
    for item in feed['items']:
        feed_list.append("<li><a href='%s' target='blank'>%s</a> %s/%s/%s</li>" % (item['link'], item['title'], 
                        item['date_parsed'][2], item['date_parsed'][1], item['date_parsed'][0] 
                        ))
