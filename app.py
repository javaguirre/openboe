# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
import os
from datetime import datetime
import re

from app_modules.db import Db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("myconf.py")
    return app


app = create_app()


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
        else:
            filter_by['q'] = request.form['q']
        try:
            start = datetime.strptime(request.form['from'], "%m/%d/%Y")
            end = datetime.strptime(request.form['to'], "%m/%d/%Y")
            filter_by['from_date'] = start
            filter_by['to_date'] = end
        except ValueError:
            pass

    if 'q' in filter_by:
        query = {"title": re.compile(filter_by['q'], re.IGNORECASE)}

        if "start" and "end" in filter_by:
            query['date'] = {"$gte": filter_by['start'], "$lte": filter_by['to_date']}

        links = Db().has('link', query)
    else:
        links = Db().has('link', {"feed_id": feed['_id']})

    return render_template("feeds.html",
                           links=links, query=filter_by, feed_slug=feed_slug, sections=sections, feeds=feeds)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', app.config['PORT']))
    app.run(host='0.0.0.0', port=port)
