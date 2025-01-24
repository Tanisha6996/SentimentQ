# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import pickle
# import time
# import os

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


from flask import Flask, render_template, request, jsonify
import pandas as pd
import time
import re
import csv
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from generic_nlp import GenericNLPAnalyzer
from nltk import download
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import pickle

# Flask app setup
app = Flask(__name__, template_folder="templates")

# # Download NLTK resources
# download('stopwords')
# download('vader_lexicon')

# # Initialize stopwords and VADER
# stop_words = set(stopwords.words('english'))
# sia = SentimentIntensityAnalyzer()

# # Mental Health Keywords
# mental_health_keywords = [
#     "anxiety", "depression", "stress", "mental health", "therapy",
#     "mindfulness", "wellness", "self-care", "emotional health", "mental illness",
#     "happiness", "joy", "gratitude", "resilience", "positivity", "calm",
#     "relaxation", "hope", "optimism", "contentment", "fatigue", "panic",
#     "overthinking", "restlessness", "irritability", "insomnia", "burnout", "fear",
#     "loneliness", "isolation", "psychologist", "counselor", "psychiatry",
#     "therapy session", "mental health support", "coping mechanisms",
#     "stress management", "yoga", "journaling", "exercise", "healthy diet",
#     "#MentalHealth", "#SelfCare", "#Wellness", "#Mindfulness"
# ]

# # Preprocessing Function
# def preprocess_and_encode(tweets, keywords):
#     def clean_tweet(tweet):
#         tweet = re.sub(r"http\S+", "", tweet)  # Remove URLs
#         tweet = re.sub(r"[^a-zA-Z\s]", "", tweet)  # Remove special characters
#         tweet = tweet.lower().strip()
#         tweet = " ".join([word for word in tweet.split() if word not in stop_words])
#         return tweet

#     def contains_keyword(tweet, keywords):
#         return any(keyword in tweet for keyword in keywords)

#     binary_states = []
#     for tweet in tweets:
#         cleaned_tweet = clean_tweet(tweet)
#         binary_states.append(1 if contains_keyword(cleaned_tweet, keywords) else 0)
#     return binary_states

# # Grover's Algorithm Logic
# def grover_search(tweets):
#     binary_states = preprocess_and_encode(tweets, mental_health_keywords)
#     if not any(binary_states):
#         return []

#     backend = Aer.get_backend('qasm_simulator')
#     n = len(binary_states).bit_length()
#     oracle = oracle_circuit(binary_states)
#     grover_qc = grover_circuit(n, oracle)
#     grover_qc.measure_all()
#     job = backend.run(grover_qc, shots=1024)
#     result = job.result()
#     counts = result.get_counts()

#     indices = [int(key, 2) for key, value in counts.items() if value > 0]
#     valid_indices = sorted([index for index in indices if index < len(binary_states) and binary_states[index] == 1])
#     return valid_indices

# # Define Oracle Circuit
# def oracle_circuit(binary_states):
#     n = len(binary_states).bit_length()
#     oracle = QuantumCircuit(n)
#     for i, state in enumerate(binary_states):
#         if state == 1:
#             binary_string = bin(i)[2:].zfill(n)
#             for j, bit in enumerate(binary_string):
#                 if bit == '0':
#                     oracle.x(j)
#             oracle.mcx(list(range(n - 1)), n - 1)  # Multi-controlled Z gate
#             for j, bit in enumerate(binary_string):
#                 if bit == '0':
#                     oracle.x(j)
#     return oracle

# # Define Grover Circuit
# def grover_circuit(n, oracle):
#     qc = QuantumCircuit(n)
#     qc.h(range(n))
#     qc.compose(oracle, inplace=True)
#     qc.h(range(n))
#     qc.z(range(n))
#     qc.cz(0, n - 1)  # Multi-controlled Z gate
#     qc.h(range(n))
#     return qc

# # Sentiment Analysis Logic
# def analyze_sentiment(tweet):
#     score = sia.polarity_scores(tweet)
#     return 'Positive' if score['compound'] >= 0 else 'Negative'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze_generic", methods=["POST"])
def analyze_generic():
    """
    Analyze using Generic NLP (pickle file model).
    """
    try:
        file = request.files['file']
        df = pd.read_csv(file)
        tweets = df['text'].tolist()

        with open('generic_nlp_analyzer.pkl', 'rb') as f:
            generic_analyzer = pickle.load(f)

        start_time = time.time()
        sentiments = [generic_analyzer.analyze_sentiment_vader(tweet) for tweet in tweets]
        end_time = time.time()

        positive_count = sentiments.count("Positive")
        negative_count = sentiments.count("Negative")

        return jsonify({
            "time_taken": end_time - start_time,
            "positive": positive_count,
            "negative": negative_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route("/analyze_grover", methods=["POST"])
# def analyze_grover():
#     """
#     Analyze using Grover's Algorithm + Sentiment Analysis.
#     """
#     try:
#         file = request.files['file']
#         df = pd.read_csv(file)
#         tweets = df['text'].tolist()

#         start_time = time.time()
#         valid_indices = grover_search(tweets)
#         target_tweets = [tweets[i] for i in valid_indices]
#         sentiments = [analyze_sentiment(tweet) for tweet in target_tweets]
#         end_time = time.time()

#         positive_count = sentiments.count("Positive")
#         negative_count = sentiments.count("Negative")

#         return jsonify({
#             "time_taken": end_time - start_time,
#             "positive": positive_count,
#             "negative": negative_count
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
