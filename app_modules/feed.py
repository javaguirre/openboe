# -*- coding: utf-8 -*-
import feedparser
from datetime import datetime


def parse(url, filter_by={}):

    feed = feedparser.parse(url)
    feed_list = []
    filter_text = ""
    #TODO Add in template uls, format date, load image item['summary']
    try:
        filter_text = filter_by['q']
    except KeyError as msg:
        print 'Doesnt exist: %s' % msg

    print filter_text
    try:
        filter_from = filter_by['from_date']
        filter_from = datetime.strptime(filter_from, "%m/%d/%Y")
    except (ValueError, KeyError) as msg:
        print 'Doesnt exist from_date: %s' % msg
        filter_from = ""

    try:
        filter_to = filter_by['to_date']
        filter_to = datetime.strptime(filter_to, "%m/%d/%Y")
    except (ValueError, KeyError) as msg:
        print 'Doesnt exist to_date: %s' % msg
        filter_to = ""

    for item in feed['items']:
        if filter_text in item['title'].lower() or filter_text in item['description'].lower():
            item_date = item['description'].split(" - ")[1].replace("Publicado el", "").strip()
            item_date = datetime.strptime(item_date, "%d/%m/%Y")

            if filter_from and filter_to:
                if filter_from <= item_date and filter_to >= item_date:
                    feed_list.append(item)
            else:
                feed_list.append(item)

    return feed_list
