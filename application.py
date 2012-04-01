# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
import os
from datetime import datetime
import re
app = Flask(__name__)

from db import Db


@app.route("/")
def index():
    sections = Db().get_col('section')
    feeds = list(Db().get_col('feed'))

    return render_template("index.html", sections=sections, feeds=feeds)


@app.route("/<section_slug>/<feed_slug>", methods=['GET', 'POST'])
def feed(section_slug, feed_slug):
    sections = Db().get_col('section')
    feeds = list(Db().get_col('feed'))
    feed = Db().find_one('feed', {"slug": feed_slug})

    if not feed:
        abort(404)

    filter_by = {}

    if request.method == 'POST':
        if not re.match("[\s?\w\s?]+", request.form['q']):
            abort(404)
        try:
            start = datetime.strptime(request.form['from'], "%m/%d/%Y")
            end = datetime.strptime(request.form['to'], "%m/%d/%Y")
        except ValueError:
            abort(404)

        filter_by = {"q": request.form['q'],
                     "from_date": start, "to_date": end}

    if 'q' in filter_by:
        links = Db().has('link',
                         {"title": "/.*" + filter_by['q'] + ".*/i",
                          "date": {"$gte": filter_by['from_date'], "$lte": filter_by['to_date']}})
    else:
        links = Db().has('link', {"feed_id": feed['_id']})

    return render_template("feeds.html",
                           links=links, query=filter_by, feed_slug=feed_slug, sections=sections, feeds=feeds)


if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', 45412))
    app.run(host='0.0.0.0', port=port)
