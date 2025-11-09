import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import database_manager
import article

app = Flask(__name__)
CORS(app)  # This will allow all origins

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    """Returns a simple greeting message."""
    return "<h1>Local Python API Server Running</h1><p>Navigate to /api/data to see JSON output.</p>"

@app.route('/api/data/news_papers')
def get_news_papers():
    papers = database_manager.get_all_news_papers()
    return jsonify([paper.to_dict() for paper in papers])

@app.route('/api/data/news_papers/<int:news_paper_id>/articles')
def get_articles_by_news_paper(news_paper_id: int):
    articles = database_manager.get_all_articles_of_news_paper(news_paper_id)
    return jsonify([art.to_dict() for art in articles])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000, debug=True)