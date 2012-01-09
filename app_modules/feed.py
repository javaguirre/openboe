# -*- coding: utf-8 -*-
import feedparser
from datetime import datetime


def replace_all(text, dic):
    text_formatted = text
    for i, j in dic.iteritems():
        text_formatted = text_formatted.replace(i, j)
    return text_formatted


def parse(url, filter_by={}):

    feed = feedparser.parse(url)
    feed_list = []
    filter_text = ""
    reps = {u"á": u"a", u"í": u"i", u"ó": u"o", u"é": u"e", u"ú": u"u"}

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
        item_title = replace_all(item['title'].lower(), reps)
        item_desc = item['description'].lower()

        if filter_text in item_title or filter_text in item_desc:
            item_date = item['description'].split(" - ")[1].replace("Publicado el", "").strip()
            item_date = datetime.strptime(item_date, "%d/%m/%Y")

            if filter_from and filter_to:
                if filter_from <= item_date and filter_to >= item_date:
                    feed_list.append(item)
            else:
                feed_list.append(item)

    return feed_list
