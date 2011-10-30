from flask import Flask
import feed
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"
    
@app.route("/feed/<name>")
def feed(name):
    feeds = ["seccionI", "seccionII", "seccionIII", "seccionIV"]
    topics = {"becas": "", "ayudas": "", "estudio": "", "convenios": "", "divisas": "", "prestamos": "", "servicios": ""
                , "colaboracion": ""}
    if topics.has_key(name):
        print name
    else:
        
    return "My feed"

if __name__ == "__main__":
    app.run()

