# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, url_for
from app_modules.feed import parse
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"
    
@app.route("/feed/<name>", methods=['GET', 'POST'])
def feed(name):
    feeds = ["seccionI", "seccionII", "seccionIII", "seccionIV"]
    topics = {
              "becas": "http://www.boe.es/rss/canal.php?c=becas",
              "ayudas": "http://www.boe.es/rss/canal.php?c=ayudas",
              "estudio": "http://www.boe.es/rss/canal.php?c=planes",
              "convenios": "http://www.boe.es/rss/canal.php?c=ccolectivos",
              "divisas": "http://www.boe.es/rss/canal.php?c=cambios",
              "prestamos": "http://www.boe.es/rss/canal.php?c=prestamos",
              "servicios": "http://www.boe.es/rss/canal.php?c=cartas", 
              "colaboracion": "http://www.boe.es/rss/canal.php?c=ccolaboracion",
              "premios": "http://www.boe.es/rss/canal.php?c=premios"
              }
    filter_by = ""
    
    if request.method == 'POST':
        #TODO check POST['q']
        filter_by = request.form['q']

    if topics.has_key(name):
        links = parse(topics[name], filter_by)
    else:
        abort(404)
        
    return render_template("feeds.html", links=links, query=filter_by)

if __name__ == "__main__":
    app.debug = True
    app.run()
