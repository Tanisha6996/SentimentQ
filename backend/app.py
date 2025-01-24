from flask import Flask, jsonify, send_file, render_template
from quantum_search import grover_search, save_to_csv
from sentiment_analysis import analyze_tweets_from_csv
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download
import time

# Download required resources
download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

# Global variables for charts and data
sentiment_chart_buffer = BytesIO()
performance_chart_buffer = BytesIO()
last_df = None  # Holds the last DataFrame for sentiment analysis
last_hybrid_time = 0
last_nlp_time = 0

@app.route('/')
def index():
    """Render the frontend HTML page."""
    return render_template('index.html')


@app.route('/process', methods=['GET'])
def process_charts():
    """
    Serve chart URLs for sentiment analysis and performance comparison.
    """
    if not last_df:
        return jsonify({"message": "No data available. Please process tweets first."}), 400

    # Generate charts
    generate_sentiment_chart(last_df)
    generate_performance_chart(last_hybrid_time, last_nlp_time)

    return jsonify({
        "message": "Charts generated successfully!",
        "chart_urls": {
            "sentiment_chart": "/charts/sentiment",
            "performance_chart": "/charts/performance"
        }
    })


@app.route('/charts/sentiment')
def serve_sentiment_chart():
    """Serve the sentiment analysis chart as a PNG image."""
    sentiment_chart_buffer.seek(0)
    return send_file(sentiment_chart_buffer, mimetype='image/png')


@app.route('/charts/performance')
def serve_performance_chart():
    """Serve the performance comparison chart as a PNG image."""
    performance_chart_buffer.seek(0)
    return send_file(performance_chart_buffer, mimetype='image/png')


@app.route('/process_tweets', methods=['POST'])
def process_tweets():
    """
    Process tweets using Grover's Algorithm and analyze sentiments.
    """
    global last_df, last_hybrid_time, last_nlp_time

    data = request.get_json()
    tweets = data.get('tweets', [])

    if not tweets or not isinstance(tweets, list):
        return jsonify({"message": "Invalid input. Please provide a list of tweets."}), 400

    # Step 1: Grover's Algorithm
    start_hybrid = time.time()
    valid_indices = grover_search(tweets)
    hybrid_duration = time.time() - start_hybrid

    if not valid_indices:
        return jsonify({"message": "No tweets matched the keywords."}), 400

    # Step 2: Save target tweets to CSV
    target_csv = "target_tweets.csv"
    save_to_csv(target_csv, valid_indices, tweets)

    # Step 3: Sentiment Analysis
    start_nlp = time.time()
    last_df = analyze_tweets_from_csv(target_csv)
    nlp_duration = time.time() - start_nlp

    # Update performance metrics
    last_hybrid_time = hybrid_duration
    last_nlp_time = nlp_duration

    return jsonify({
        "message": "Tweets processed successfully! Use /process to view charts.",
        "num_target_tweets": len(valid_indices)
    })


def generate_sentiment_chart(df):
    """Generate and save sentiment analysis bar chart."""
    global sentiment_chart_buffer
    sentiment_counts = df['Sentiment'].value_counts()

    plt.figure(figsize=(6, 4))
    sentiment_counts.plot(kind='bar', color=['green', 'red'])
    plt.title("Sentiment Analysis of Tweets")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()

    sentiment_chart_buffer = BytesIO()
    plt.savefig(sentiment_chart_buffer, format='png')
    sentiment_chart_buffer.seek(0)
    plt.close()


def generate_performance_chart(hybrid_time, nlp_time):
    """Generate and save performance comparison bar chart."""
    global performance_chart_buffer
    labels = ['Hybrid Model (Grover + NLP)', 'NLP-Only Model']
    times = [hybrid_time, nlp_time]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, times, color=['blue', 'orange'])
    plt.title("Performance Comparison")
    plt.ylabel("Time (seconds)")
    plt.tight_layout()

    performance_chart_buffer = BytesIO()
    plt.savefig(performance_chart_buffer, format='png')
    performance_chart_buffer.seek(0)
    plt.close()


if __name__ == "__main__":
    app.run(debug=True)
