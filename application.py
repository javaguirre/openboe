from flask import Flask, render_template
from app_modules.feed import parse
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"
    
@app.route("/feed/<name>")
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
    if topics.has_key(name):
        links = parse(topics[name])
    else:
        response = "nothing"
        
    return render_template("feeds.html", links=links)

if __name__ == "__main__":
    app.debug = True
    app.run()

