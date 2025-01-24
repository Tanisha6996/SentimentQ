from flask import Flask, render_template, request, jsonify
from grover_vader_model import GroverSentimentAnalyzer
import pandas as pd
import pickle
import os
import time

# Load the GroverSentimentAnalyzer object
with open('grover_sentiment_analyzer.pkl', 'rb') as pkl_file:
    analyzer = pickle.load(pkl_file)

app = Flask(__name__, template_folder="../templates")

# Directory to save uploaded files dynamically
UPLOAD_FOLDER = './'
TARGET_TWEETS_CSV = os.path.join(UPLOAD_FOLDER, 'target_tweets.csv')
ANALYZED_TWEETS_CSV = os.path.join(UPLOAD_FOLDER, 'analyzed_tweets.csv')


@app.route('/')
def index():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/upload', methods=['POST'])
def upload_and_process():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file."}), 400

        # Process the file
        df = pd.read_csv(file)
        if 'text' not in df.columns:
            return jsonify({"error": "The uploaded file must contain a 'text' column."}), 400

        tweets = df['text'].tolist()

        # Perform Grover search and sentiment analysis
        start_grover = time.time()
        valid_indices = analyzer.grover_search(tweets)
        grover_time = time.time() - start_grover

        target_csv = os.path.join(UPLOAD_FOLDER, 'target_tweets.csv')
        analyzer.save_to_csv(target_csv, valid_indices, tweets)

        start_sentiment = time.time()
        analyzed_csv = os.path.join(UPLOAD_FOLDER, 'analyzed_tweets.csv')
        analyzed_df = analyzer.analyze_tweets_from_csv(target_csv, analyzed_csv)
        sentiment_time = time.time() - start_sentiment

        positive_count = (analyzed_df['Sentiment'] == 'Positive').sum()
        negative_count = (analyzed_df['Sentiment'] == 'Negative').sum()

        return jsonify({
            "message": "Dataset processed successfully!",
            "performance": {
                "grover_time": grover_time,
                "sentiment_time": sentiment_time
            },
            "word_counts": {
                "positive": int(positive_count),
                "negative": int(negative_count)
            }
        })
    except Exception as e:
        # Ensure the response is always JSON
        return jsonify({"error": str(e)}), 500
 

if __name__ == "__main__":
    app.run(debug=True)
