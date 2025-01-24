from flask import Flask, jsonify, request
from quantum_search import grover_search
import time

app = Flask(__name__)

# Global variables to store results
last_hybrid_time = None
last_traditional_time = None
positive_count = 0
negative_count = 0


@app.route('/process_tweets', methods=['POST'])
def process_tweets():
    """
    Process tweets using Grover's hybrid model and return performance metrics
    along with sentiment word counts (positive and negative).
    """
    global last_hybrid_time, last_traditional_time, positive_count, negative_count

    try:
        # Parse input tweets
        data = request.get_json()
        tweets = data.get('tweets', [])

        if not tweets or not isinstance(tweets, list):
            return jsonify({"message": "Invalid input. Please provide a list of tweets."}), 400

        # Step 1: Grover's Hybrid Model
        start_hybrid = time.time()
        valid_indices = grover_search(tweets)

        if not valid_indices:
            return jsonify({"message": "No tweets matched the keywords."}), 400

        last_hybrid_time = time.time() - start_hybrid

        # Count positive and negative tweets for the hybrid model
        positive_count = len([i for i in valid_indices if "positive" in tweets[i].lower()])
        negative_count = len([i for i in valid_indices if "negative" in tweets[i].lower()])

        # Step 2: Traditional NLP-only Sentiment Analysis
        start_traditional = time.time()
        # Placeholder for traditional NLP processing
        time.sleep(0.5)  # Simulating NLP processing time
        last_traditional_time = time.time() - start_traditional

        # Return performance metrics and word counts
        return jsonify({
            "message": "Tweets processed successfully!",
            "performance": {
                "hybrid_time": last_hybrid_time,
                "traditional_time": last_traditional_time
            },
            "word_counts": {
                "positive": positive_count,
                "negative": negative_count
            }
        })

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
