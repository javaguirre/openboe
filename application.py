# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, url_for
from app_modules.feed import parse
app = Flask(__name__)

RSS_URL = "http://www.boe.es/rss/"

topics = {
          "url": "canal.php",
          "becas": "?c=becas",
          "ayudas": "?c=ayudas",
          "estudio": "?c=planes",
          "convenios": "?c=ccolectivos",
          "divisas": "?c=cambios",
          "prestamos": "?c=prestamos",
          "servicios": "?c=cartas",
          "colaboracion": "?c=ccolaboracion",
          "premios": "?c=premios"
          }

boes = {
          "url": "boe.php",
          "sumario": "",
          "seccionI": "?s=1",
          "seccionII": "?s=2",
          "seccionIIA": "?s=2A",
          "seccionIIB": "?s=SB",
          "seccionIII": "?s=3",
          "seccionIV": "?s=4",
          "seccionV": "?s=5",
          "seccionVA": "?s=5A",
          "seccionVB": "?s=5B",
          "seccionVC": "?s=5C",
          "suplemento": "?s=T"
        }

bormes = {
          "url": "borme.php",
          "sumario": "",
          "seccionI": "?s=1",
          "seccionIA": "?s=A",
          "seccionIB": "?s=B",
          "seccionII": "?s=C"
        }


#FIXME move it to somewhere
def treat_request(type_feed, request, name):
    filter_by = {}

    if type_feed == "boe":
        rss_topics = boes
    elif type_feed == 'borme':
        rss_topics = bormes
    else:
        rss_topics = topics

    if request.method == 'POST':
        #TODO check POST['q']
        filter_by = {"q": request.form['q'],
                     "from_date": request.form['from'], "to_date": request.form['to']}

    if name in rss_topics:
        links = parse(RSS_URL + rss_topics['url'] + rss_topics[name], type_feed, filter_by)
    else:
        abort(404)

    return filter_by, links


@app.route("/")
def index():
    return render_template("index.html", topics=topics)


@app.route("/feed/<name>", methods=['GET', 'POST'])
def feed(name):
    filter_by, links = treat_request('topics', request, name)

    return render_template("feeds.html",
                           links=links, query=filter_by, topics=topics, bormes=bormes, boes=boes, name=name)


@app.route("/borme/<name>", methods=['GET', 'POST'])
def borme(name):
    filter_by, links = treat_request('borme', request, name)

    return render_template("feeds.html",
                           links=links, query=filter_by, topics=topics, bormes=bormes, boes=boes, name=name)


@app.route("/boe/<name>", methods=['GET', 'POST'])
def boe(name):
    filter_by, links = treat_request('boe', request, name)

    return render_template("feeds.html",
                           links=links, query=filter_by, topics=topics, bormes=bormes, boes=boes, name=name)


if __name__ == "__main__":
    app.debug = True
    app.run()
