import pickle
from grover_vader_model import GroverSentimentAnalyzer
from generic_nlp import GenericNLPAnalyzer

try:
    with open('/home/tanisha/Documents/GitHub/AlgoRythms/backend/grover_sentiment_analyzer.pkl', 'rb') as pkl_file:
        grover_analyzer = pickle.load(pkl_file)
    print("Grover Sentiment Analyzer loaded successfully.")
except Exception as e:
    print(f"Error loading grover_sentiment_analyzer.pkl: {e}")

try:
    with open('/home/tanisha/Documents/GitHub/AlgoRythms/backend/generic_nlp_analyzer.pkl', 'rb') as pkl_file:
        generic_analyzer = pickle.load(pkl_file)
    print("Generic Sentiment Analyzer loaded successfully.")
except Exception as e:
    print(f"Error loading generic_sentiment_analyzer.pkl: {e}")
