# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import pickle
# import time
# import os
# from grover_vader_model import GroverSentimentAnalyzer
# from generic_nlp import GenericNLPAnalyzer

# # Load the two models from pickle files
# try:
#     with open('/home/tanisha/Documents/GitHub/AlgoRythms/backend/grover_sentiment_analyzer.pkl', 'rb') as pkl_file:
#         grover_analyzer = pickle.load(pkl_file)
#     with open('/home/tanisha/Documents/GitHub/AlgoRythms/backend/generic_nlp_analyzer.pkl', 'rb') as pkl_file:
#         generic_analyzer = pickle.load(pkl_file)
# except Exception as e:
#     print(f"Error loading pickle files: {str(e)}")
#     grover_analyzer = None
#     generic_analyzer = None

# app = Flask(__name__, template_folder="../templates")

# @app.route('/')
# def index():
#     return render_template('index2.html')

# # Directory to save uploaded files dynamically
# UPLOAD_FOLDER = './uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload_and_process():
#     """
#     Handle dataset upload, process with both models, and return results.
#     """
#     try:
#         if grover_analyzer is None or generic_analyzer is None:
#             return jsonify({"error": "Models are not loaded properly. Check the backend."}), 500

#         # Validate file upload
#         if 'file' not in request.files:
#             return jsonify({"error": "No file uploaded."}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No file selected."}), 400

#         # Save the uploaded file
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         # Load dataset
#         df = pd.read_csv(file_path)
#         if 'text' not in df.columns:
#             return jsonify({"error": "The uploaded file must contain a 'text' column."}), 400

# #         tweets = df['text'].tolist()

# #         # Run Grover's algorithm
# #         start_grover = time.time()
# #         valid_indices = grover_analyzer.grover_search(tweets)
# #         grover_time = time.time() - start_grover

# #         grover_analyzer.save_to_csv('grover_target_tweets.csv', valid_indices, tweets)
# #         grover_results = grover_analyzer.analyze_tweets_from_csv('grover_target_tweets.csv', 'grover_analyzed_tweets.csv')

# #         grover_positive = (grover_results['Sentiment'] == 'Positive').sum()
# #         grover_negative = (grover_results['Sentiment'] == 'Negative').sum()

# #         # Run Generic NLP
# #         start_generic = time.time()
# #         generic_results = pd.DataFrame({
# #             "Tweet": tweets,
# #             "Sentiment": [generic_analyzer.analyze_sentiment(tweet) for tweet in tweets]
# #         })
# #         generic_time = time.time() - start_generic

# #         generic_positive = (generic_results['Sentiment'] == 'Positive').sum()
# #         generic_negative = (generic_results['Sentiment'] == 'Negative').sum()

# #         # Return results
# #         return jsonify({
# #             "message": "Dataset processed successfully!",
# #             "performance": {
# #                 "grover_time": grover_time,
# #                 "generic_time": generic_time
# #             },
# #             "sentiment_counts": {
# #                 "grover": {
# #                     "positive": int(grover_positive),
# #                     "negative": int(grover_negative)
# #                 },
# #                 "generic": {
# #                     "positive": int(generic_positive),
# #                     "negative": int(generic_negative)
# #                 }
# #             }
# #         })

# #     except Exception as e:
# #         print(f"Error during processing: {e}")
# #         return jsonify({"error": str(e)}), 500
    
# # if __name__ == "__main__":
# #     app.run(debug=True)



# # # Helper Function: Process Sentiment Using TextBlob
# # def process_sentiment_textblob(data):
# #     sentiments = {"Positive": 0, "Negative": 0}
# #     for text in data:
# #         polarity = TextBlob(text).sentiment.polarity
# #         if polarity > 0:
# #             sentiments["Positive"] += 1
# #         else:
# #             sentiments["Negative"] += 1
# #     return sentiments








# from flask import Flask, request, render_template, jsonify
# import pandas as pd
# import pickle
# import time
# import plotly.express as px
# import plotly.io as pio
# from grover_vader_model import GroverSentimentAnalyzer
# from generic_nlp import GenericNLPAnalyzer


# app = Flask(__name__, template_folder="templates")

# # Load models
# try:
#     with open("grover_sentiment_analyzer.pkl", "rb") as f:
#         grover_analyzer = pickle.load(f)
#     with open("generic_nlp_analyzer.pkl", "rb") as f:
#         generic_analyzer = pickle.load(f)
#     print("Models loaded successfully.")
# except Exception as e:
#     print(f"Error loading models: {e}")
#     grover_analyzer, generic_analyzer = None, None

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/process", methods=["POST"])
# def process_file():
#     try:
#         if "file" not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400

#         file = request.files["file"]
#         if file.filename == "":
#             return jsonify({"error": "No selected file"}), 400

#         df = pd.read_csv(file)
#         if "text" not in df.columns:
#             return jsonify({"error": "The file must contain a 'text' column."}), 400

#         tweets = df["text"].tolist()

#         # Grover's Model
#         start_grover = time.time()
#         valid_indices = grover_analyzer.grover_search(tweets)
#         grover_results = grover_analyzer.analyze_tweets_from_csv(
#             "grover_target_tweets.csv", "grover_analyzed_tweets.csv"
#         )
#         grover_time = time.time() - start_grover

#         grover_positive = (grover_results["Sentiment"] == "Positive").sum()
#         grover_negative = (grover_results["Sentiment"] == "Negative").sum()

#         # Generic NLP Model
#         start_generic = time.time()
#         generic_sentiments = [
#             generic_analyzer.analyze_sentiment(tweet) for tweet in tweets
#         ]
#         generic_time = time.time() - start_generic
#         generic_positive = sum(1 for sentiment in generic_sentiments if sentiment == 1)
#         generic_negative = sum(1 for sentiment in generic_sentiments if sentiment == 0)

#         return jsonify(
#             {
#                 "grover": {"time": grover_time, "positive": grover_positive, "negative": grover_negative},
#                 "generic": {"time": generic_time, "positive": generic_positive, "negative": generic_negative},
#             }
#         )

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
from generic_nlp import GenericNLPAnalyzer


app = Flask(__name__, template_folder="templates")

# Load the Generic NLP model
try:
    with open('generic_nlp_analyzer.pkl', 'rb') as f:
        generic_analyzer = pickle.load(f)
    print("Generic NLP Analyzer loaded successfully.")
except Exception as e:
    print(f"Error loading Generic NLP Analyzer: {e}")
    generic_analyzer = None


@app.route('/')
def index():
    """
    Serve the HTML page.
    """
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    """
    Handle file upload and process with Generic NLP Analyzer.
    """
    try:
        # Check if the model is loaded
        if generic_analyzer is None:
            return jsonify({"error": "Generic NLP Analyzer is not loaded properly."}), 500

        # Validate file upload
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected."}), 400

        # Read the uploaded file
        df = pd.read_csv(file)
        if 'text' not in df.columns:
            return jsonify({"error": "The uploaded file must contain a 'text' column."}), 400

        # Extract text data
        tweets = df['text'].tolist()

        # Perform sentiment analysis
        sentiments = [generic_analyzer.analyze_sentiment_vader(tweet) for tweet in tweets]
        positive_count = sum(1 for sentiment in sentiments if sentiment == 1)  # Assuming 1 = Positive
        negative_count = sum(1 for sentiment in sentiments if sentiment == 0)  # Assuming 0 = Negative

        # Return results
        return jsonify({
            "message": "File processed successfully!",
            "sentiment_counts": {
                "positive": positive_count,
                "negative": negative_count
            }
        })

    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
