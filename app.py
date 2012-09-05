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
    sections = list(Db().get_col('section'))
    feeds = list(Db().get_col('feed'))

    return render_template("index.html", sections=sections, feeds=feeds)


@app.route("/links/", methods=['GET', 'POST'])
def feed():
    feed_slug = request.args.get('feed', '')
    feed = Db().find_one('feed', {"slug": feed_slug})

    if not feed:
        abort(404)

    filter_by = {}
    query = request.args.get('q', None)
    from_date = request.args.get('from', None)
    to_date = request.args.get('to', None)

    if query:
        if not re.match("[\s?\w\s?]+", query):
            abort(404)
        else:
            filter_by['q'] = query
        try:
            if from_date and to_date:
                start = datetime.strptime(from_date, "%m-%d-%Y")
                end = datetime.strptime(to_date, "%m-%d-%Y")
                filter_by['from_date'] = start
                filter_by['to_date'] = end
        except ValueError:
            pass

    if 'q' in filter_by:
        q_regex = re.compile(filter_by['q'], re.IGNORECASE)
        db_query = {"feed_id": feed['_id'],
                    "$or": [{"title": q_regex}, {"description": q_regex}]}

        if "start" and "end" in filter_by:
            db_query['date'] = {"$gte": filter_by['start'], "$lte": filter_by['to_date']}
    else:
        db_query = {"feed_id": feed['_id']}

    links = Db().has('link', db_query, sort_field='date')
    return  make_json_response(links)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', app.config['PORT']))
    app.run(host='0.0.0.0', port=port)
