import mechanize
from lxml.html import document_fromstring
from time import time
from db import Db


DIV_FEED_CLASSES = ["cajaRSSboe", "cajaRSSborme"]
BOE_URL = "http://www.boe.es/rss/"
db_obj = Db()

response = mechanize.urlopen(BOE_URL)
content_tree = document_fromstring(response.read())

div_boxes = []
feeds = []
titles = []

for div_class in DIV_FEED_CLASSES:
    print div_class
    content_tree_elem = content_tree.find_class(div_class)
    div_boxes.extend([content_elem for content_elem in content_tree_elem])

for div_box in div_boxes:
    feeds.extend(div_box.find_class('listaFeeds'))
    titles.extend(div_box.findall('h3'))

    #print elem.text_content()
    #print div_box.find_tag('h3')
for feed, title in zip(feeds, titles):
    print titles
    print db_obj.has('section', {"title": title.text_content()})
    if not db_obj.has('section', {"title": title.text_content()}):
        section_obj = db_obj.insert('section',
                                    {"title": title.text_content(), "timestamp": time.time()})
        print section_obj
    #rss_list.append(link)
    #print title.text_content()
    for elem in feed.iterlinks():
        if not db_obj.has('feed', {"url": elem[2]}):
            db_obj.insert('feed',
                          {"title": elem[0].text_content(), "url": elem[2],
                           "section_id": section_obj['_id']
                          })
