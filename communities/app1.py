from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/communityDB"
mongo = PyMongo(app)

# MongoDB collection
articles_collection = mongo.db.articles

# Insert dummy data if collection is empty
def insert_dummy_data():
    if articles_collection.count_documents({}) == 0:
        dummy_articles = [
            {
                "username": "Alice",
                "title": "The Future of AI",
                "content": "Artificial intelligence is transforming industries worldwide.",
                "timestamp": datetime.utcnow()
            },
            {
                "username": "Bob",
                "title": "Understanding Climate Change",
                "content": "Climate change is a pressing issue that requires global attention.",
                "timestamp": datetime.utcnow()
            },
            {
                "username": "Charlie",
                "title": "Healthy Eating Habits",
                "content": "Maintaining a balanced diet is crucial for overall health.",
                "timestamp": datetime.utcnow()
            }
        ]
        articles_collection.insert_many(dummy_articles)

insert_dummy_data()

@app.route('/community')
def community():
    try:
        # Retrieve all articles from the database
        articles = list(articles_collection.find().sort("timestamp", -1))
    except Exception as e:
        return f"An error occurred while retrieving articles: {str(e)}", 500

    return render_template('community.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
