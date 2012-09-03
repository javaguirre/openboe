# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
import os
from datetime import datetime
import re

from app_modules.db import Db
from app_modules.utils import make_json_response


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


@app.route("/links/", methods=['GET', 'POST'])
def feed():
    feed_slug = request.args.get('feed', '')
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
        q_regex = re.compile(filter_by['q'], re.IGNORECASE)
        query = {"$or": [{"title": q_regex}, {"description": q_regex}]}

        if "start" and "end" in filter_by:
            query['date'] = {"$gte": filter_by['start'], "$lte": filter_by['to_date']}

        links = Db().has('link', query, sort_field="date")
    else:
        links = Db().has('link', {"feed_id": feed['_id']}, sort_field="date")

    #return render_template("feeds.html",
                           #links=links, query=filter_by, feed_slug=feed_slug, sections=sections, feeds=feeds)
    return  make_json_response(links)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', app.config['PORT']))
    app.run(host='0.0.0.0', port=port)
