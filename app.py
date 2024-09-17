from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS
import spacy
from transformers import pipeline
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize BERT sentiment analysis pipeline
sentiment_model = pipeline('sentiment-analysis')

NEWS_API_KEY = '2d833531d4d44c048a8b201e33e8d39f'

# Initialize SQLite DB for comments
def init_db():
    conn = sqlite3.connect('comments.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS comments
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id TEXT NOT NULL,
        user_name TEXT NOT NULL,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
    conn.close()

init_db()

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
    return keywords

@app.route('/')
def index():
    return render_template('news.html')

@app.route('/api/news')
def get_news_data():
    category = request.args.get('category', 'general')
    url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news_data = response.json()

    for article in news_data.get('articles', []):
        headline = article.get('title', '')

        if headline:
            sentiment = sentiment_model(headline)[0]
            sentiment_label = 'Positive' if sentiment['label'] == 'LABEL_1' else 'Negative'
            
            article['flash_alert'] = {
                'headline': f"Flash Alert: {headline}",
                'sentiment': {
                    'label': sentiment_label,
                    'score': round(sentiment['score'], 2)
                },
                'keywords': extract_keywords(headline)
            }
        else:
            article['flash_alert'] = {
                'headline': 'Flash Alert: No Headline Available',
                'sentiment': {'label': 'Neutral', 'score': 0.5},
                'keywords': []
            }

    return jsonify(news_data)

# Comment submission route
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.json
    article_id = data['article_id']
    user_name = data['user_name']
    comment = data['comment']
    
    conn = sqlite3.connect('comments.db')
    conn.execute("INSERT INTO comments (article_id, user_name, comment) VALUES (?, ?, ?)", 
                 (article_id, user_name, comment))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
