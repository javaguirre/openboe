# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, url_for
import os
app = Flask(__name__)

from db import Db


#FIXME move it to somewhere
def treat_request(type_feed, request, name):
    filter_by = {}

    if request.method == 'POST':
        #TODO check POST['q']
        filter_by = {"q": request.form['q'],
                     "from_date": request.form['from'], "to_date": request.form['to']}

    if name in "hola":
        #links = parse(RSS_URL + rss_topics['url'] + rss_topics[name], type_feed, filter_by)
        pass
    else:
        abort(404)

    return filter_by, []


@app.route("/")
def index():
    sections = Db().get_col('section')
    feeds = list(Db().get_col('feed'))

    return render_template("index.html", sections=sections, feeds=feeds)


@app.route("/<section>/<name>", methods=['GET', 'POST'])
def feed(name):
    links = Db().has('link', {"feed_id": feed_id})
    filter_by = 'nothing'

    return render_template("feeds.html",
                           links=links, query=filter_by, name=name)


if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', 45412))
    app.run(host='0.0.0.0', port=port)
