import feedparser
from datetime import datetime
import mechanize
from lxml.html import document_fromstring
from time import time

from utils import slug
from db import Db


def insert_feed_items():
    '''
        Retrieves items in feeds saved before in our DB. If
        items were in the DB before, it ignores them
    '''

    URL = 'http://www.boe.es'
    db_obj = Db()
    feeds = db_obj.get_col('feed')

    for feed in feeds:
        feed_obj = feedparser.parse("".join([URL, feed['url']]))

        for item in feed_obj['items']:
            if not db_obj.has('link', {"link": item['link']}):
                date_item = item['description'].split(" - ")[1].replace("Publicado el", "").strip()

                try:
                    date_item = datetime.strptime(date_item, "%d/%m/%Y")
                except ValueError:
                    date_item = "0000"

                db_obj.insert('link',
                              {"title": item['title'],
                               "description": item['description'],
                               'guid': item['guid'], 'link': item['link'],
                               "date": date_item,
                               "feed_id": feed['_id']
                              })


def get_rss_urls():
    '''
        Retrieves the name and the url from all RSS
        in the BOE's site and saves them in a mongo collection
    '''

    DIV_FEED_CLASSES = ["cajaRSSboe", "cajaRSSborme"]
    BOE_URL = "http://www.boe.es/rss/"
    db_obj = Db()

    response = mechanize.urlopen(BOE_URL)
    content_tree = document_fromstring(response.read())

    div_boxes = []
    feeds = []
    titles = []

    for div_class in DIV_FEED_CLASSES:
        content_tree_elem = content_tree.find_class(div_class)
        div_boxes.extend([content_elem for content_elem in content_tree_elem])

    for div_box in div_boxes:
        feeds.extend(div_box.find_class('listaFeeds'))
        titles.extend(div_box.findall('h3'))

    for feed, title in zip(feeds, titles):
        section_obj = db_obj.has('section', {"title": title.text_content()})

        if not section_obj and title.text_content():
            section_obj = db_obj.insert('section',
                                        {"title": title.text_content(), "timestamp": time(),
                                         "slug": slug(title.text_content())
                                        })
        else:
            section_obj = section_obj[0]
            #TODO update timestamp

        if section_obj:
            for elem in feed.iterlinks():
                if not db_obj.has('feed', {"url": elem[2]}):
                    db_obj.insert('feed',
                                  {"title": elem[0].text_content(), "url": elem[2],
                                   "section_id": section_obj['_id'],
                                   "slug": slug(elem[0].text_content())
                                  })
