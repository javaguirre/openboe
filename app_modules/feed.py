# -*- coding: utf-8 -*-
import feedparser


def parse(url, filter_by=""):

    feed = feedparser.parse(url)
    feed_list = []
    #TODO Add in template uls, format date, load image item['summary']

    for item in feed['items']:
        if filter_by in item['title'].lower():
            feed_list.append(item)

    return feed_list
