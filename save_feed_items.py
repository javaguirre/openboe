from db import Db
import feedparser
from datetime import datetime

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
