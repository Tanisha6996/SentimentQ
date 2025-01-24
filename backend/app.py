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

#         tweets = df['text'].tolist()

#         # Run Grover's algorithm
#         start_grover = time.time()
#         valid_indices = grover_analyzer.grover_search(tweets)
#         grover_time = time.time() - start_grover

#         grover_analyzer.save_to_csv('grover_target_tweets.csv', valid_indices, tweets)
#         grover_results = grover_analyzer.analyze_tweets_from_csv('grover_target_tweets.csv', 'grover_analyzed_tweets.csv')

#         grover_positive = (grover_results['Sentiment'] == 'Positive').sum()
#         grover_negative = (grover_results['Sentiment'] == 'Negative').sum()

#         # Run Generic NLP
#         start_generic = time.time()
#         generic_results = pd.DataFrame({
#             "Tweet": tweets,
#             "Sentiment": [generic_analyzer.analyze_sentiment(tweet) for tweet in tweets]
#         })
#         generic_time = time.time() - start_generic

#         generic_positive = (generic_results['Sentiment'] == 'Positive').sum()
#         generic_negative = (generic_results['Sentiment'] == 'Negative').sum()

#         # Return results
#         return jsonify({
#             "message": "Dataset processed successfully!",
#             "performance": {
#                 "grover_time": grover_time,
#                 "generic_time": generic_time
#             },
#             "sentiment_counts": {
#                 "grover": {
#                     "positive": int(grover_positive),
#                     "negative": int(grover_negative)
#                 },
#                 "generic": {
#                     "positive": int(generic_positive),
#                     "negative": int(generic_negative)
#                 }
#             }
#         })

#     except Exception as e:
#         print(f"Error during processing: {e}")
#         return jsonify({"error": str(e)}), 500
    
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify
import pandas as pd
import pickle
import time
import plotly.express as px
import plotly.io as pio
from textblob import TextBlob
from grover_vader_model import GroverSentimentAnalyzer
from generic_nlp import GenericNLPAnalyzer


app = Flask(__name__)

# Load the models
model1_path = "/home/tanisha/Documents/GitHub/AlgoRythms/backend/grover_sentiment_analyzer.pkl"  # Update path
model2_path = "/home/tanisha/Documents/GitHub/AlgoRythms/backend/generic_nlp_analyzer.pkl"  # Update path

try:
    with open(model1_path, "rb") as f:
        model1 = pickle.load(f)

    with open(model2_path, "rb") as f:
        model2 = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")
    model1, model2 = None, None

# Helper Function: Process Sentiment Using TextBlob
def process_sentiment_textblob(data):
    sentiments = {"Positive": 0, "Negative": 0}
    for text in data:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0:
            sentiments["Positive"] += 1
        else:
            sentiments["Negative"] += 1
    return sentiments

# Helper Function: Process Sentiment with Model
def process_sentiment_model(model, data):
    sentiments = {"Positive": 0, "Negative": 0}
    for text in data:
        prediction = model.predict([text])[0]
        if prediction == 1:  # Assuming 1 means positive
            sentiments["Positive"] += 1
        else:  # Assuming 0 means negative
            sentiments["Negative"] += 1
    return sentiments

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Unsupported file format. Please upload a CSV file."}), 400

    # Read the CSV file
    df = pd.read_csv(file)
    if "Text" not in df.columns:
        return jsonify({"error": "The file must contain a 'Tweet' column."}), 400

    texts = df["Text"].astype(str)

    # Process with TextBlob
    start_blob = time.time()
    blob_sentiment = process_sentiment_textblob(texts)
    end_blob = time.time()
    blob_time = end_blob - start_blob

    # Process with Model 1
    start_model1 = time.time()
    model1_sentiment = process_sentiment_model(model1, texts) if model1 else {"Positive": 0, "Negative": 0}
    end_model1 = time.time()
    model1_time = end_model1 - start_model1 if model1 else 0

    # Process with Model 2
    start_model2 = time.time()
    model2_sentiment = process_sentiment_model(model2, texts) if model2 else {"Positive": 0, "Negative": 0}
    end_model2 = time.time()
    model2_time = end_model2 - start_model2 if model2 else 0

    # Create Bar Graphs
    time_data = pd.DataFrame({
        "Model": ["TextBlob", "Model 1", "Model 2"],
        "Time (s)": [blob_time, model1_time, model2_time]
    })
    time_chart = px.bar(time_data, x="Model", y="Time (s)", title="Processing Time Comparison")
    time_chart_html = pio.to_html(time_chart, full_html=False)

    sentiment_data = pd.DataFrame({
        "Sentiment": ["Positive", "Negative"],
        "TextBlob": [blob_sentiment["Positive"], blob_sentiment["Negative"]],
        "Model 1": [model1_sentiment["Positive"], model1_sentiment["Negative"]],
        "Model 2": [model2_sentiment["Positive"], model2_sentiment["Negative"]]
    })
    sentiment_chart_blob = px.bar(
        sentiment_data, x="Sentiment", y=["TextBlob", "Model 1", "Model 2"], barmode="group",
        title="Sentiment Analysis Comparison"
    )
    sentiment_chart_html = pio.to_html(sentiment_chart_blob, full_html=False)

    # Render Results
    return render_template(
        "result.html",
        time_chart=time_chart_html,
        sentiment_chart=sentiment_chart_html
    )

if __name__ == "_main_":
    app.run(debug=True)