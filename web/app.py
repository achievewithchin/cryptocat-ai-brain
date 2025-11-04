from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CryptoCat Intelligence Web Service is running 🧠"
