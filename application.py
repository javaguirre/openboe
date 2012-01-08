# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, url_for
from app_modules.feed import parse
app = Flask(__name__)

topics = {
          "becas": "/rss/canal.php?c=becas",
          "ayudas": "/rss/canal.php?c=ayudas",
          "estudio": "/rss/canal.php?c=planes",
          "convenios": "/rss/canal.php?c=ccolectivos",
          "divisas": "/rss/canal.php?c=cambios",
          "prestamos": "/rss/canal.php?c=prestamos",
          "servicios": "/rss/canal.php?c=cartas",
          "colaboracion": "/rss/canal.php?c=ccolaboracion",
          "premios": "/rss/canal.php?c=premios"
          }


@app.route("/")
def index():
    return render_template("index.html", topics=topics)


@app.route("/feed/<name>", methods=['GET', 'POST'])
def feed(name):
    feeds = ["seccionI", "seccionII", "seccionIII", "seccionIV"]

    filter_by = {}

    if request.method == 'POST':
        #TODO check POST['q']
        filter_by = {"q": request.form['q'],
                     "from_date": request.form['from'], "to_date": request.form['to']}

    if name in topics:
        links = parse("http://www.boe.es" + topics[name], filter_by)
    else:
        abort(404)

    return render_template("feeds.html",
                           links=links, query=filter_by, topics=topics)

if __name__ == "__main__":
    app.debug = True
    app.run()
