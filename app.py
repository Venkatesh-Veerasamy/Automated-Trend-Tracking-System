from flask import Flask, render_template, jsonify
from selenium_script import get_google_trends
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_trends"]
collection = db["trends"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    result = get_trending_topics()
    return jsonify(result)

@app.route("/get-results")
def get_results():
    data = list(collection.find().sort("timestamp", -1).limit(1))
    if data:
        return jsonify(data[0])
    return jsonify({"message": "No data found"})

if __name__ == "__main__":
    app.run(debug=True)
