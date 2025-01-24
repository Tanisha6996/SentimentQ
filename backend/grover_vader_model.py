import re
import pickle
import time
import pandas as pd
import csv
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download
from qiskit import QuantumCircuit
from qiskit_aer import Aer

# Download required resources
download('stopwords')
download('vader_lexicon')

class GroverSentimentAnalyzer:
    def __init__(self):
        # Initialize keywords, stopwords, and VADER sentiment analyzer
        self.mental_health_keywords = [
            "anxiety", "depression", "stress", "mental health", "therapy",
            "mindfulness", "wellness", "self-care", "emotional health", "mental illness",
            "happiness", "joy", "gratitude", "resilience", "positivity", "calm",
            "relaxation", "hope", "optimism", "contentment", "fatigue", "panic",
            "overthinking", "restlessness", "irritability", "insomnia", "burnout", "fear",
            "loneliness", "isolation", "psychologist", "counselor", "psychiatry",
            "therapy session", "mental health support", "coping mechanisms",
            "stress management", "yoga", "journaling", "exercise", "healthy diet",
            "#MentalHealth", "#SelfCare", "#Wellness", "#Mindfulness"
        ]
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()

    def preprocess_and_encode(self, tweets):
        """
        Preprocess and encode tweets as binary states for Grover's algorithm.
        """
        def clean_tweet(tweet):
            tweet = re.sub(r"http\S+", "", tweet)  # Remove URLs
            tweet = re.sub(r"[^a-zA-Z\s]", "", tweet)  # Remove special characters
            tweet = tweet.lower().strip()
            return " ".join([word for word in tweet.split() if word not in self.stop_words])

        def contains_keyword(tweet, keywords):
            return any(keyword in tweet for keyword in keywords)

        binary_states = []
        for tweet in tweets:
            cleaned_tweet = clean_tweet(tweet)
            binary_states.append(1 if contains_keyword(cleaned_tweet, self.mental_health_keywords) else 0)
        return binary_states

    def save_to_csv(self, file_name, valid_indices, tweets):
        """
        Save target tweets to a CSV file.
        """
        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Index", "Tweet"])  # Header
                for index in valid_indices:
                    writer.writerow([index, tweets[index]])
            print(f"Target tweets successfully saved to {file_name}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def oracle_circuit(self, binary_states):
        """
        Create the oracle circuit based on binary states.
        """
        n = len(binary_states).bit_length()  # Number of qubits needed
        oracle = QuantumCircuit(n)
        for i, state in enumerate(binary_states):
            if state == 1:  # Only process states with 1
                binary_string = bin(i)[2:].zfill(n)
                for j, bit in enumerate(binary_string):
                    if bit == '0':
                        oracle.x(j)  # Flip qubit for |0>
                oracle.mcx(list(range(n - 1)), n - 1)  # Multi-controlled Z gate
                for j, bit in enumerate(binary_string):
                    if bit == '0':
                        oracle.x(j)  # Un-flip qubit
        return oracle

    def grover_circuit(self, n, oracle):
        """
        Construct Grover's Algorithm circuit.
        """
        qc = QuantumCircuit(n)
        qc.h(range(n))  # Apply H-gates to all qubits
        qc.compose(oracle, inplace=True)  # Apply Oracle
        qc.h(range(n))
        qc.z(range(n))
        qc.cz(0, n - 1)  # Multi-controlled Z gate
        qc.h(range(n))
        return qc

    def grover_search(self, tweets):
        """
        Perform Grover's search on the tweets.
        """
        binary_states = self.preprocess_and_encode(tweets)
        if not any(binary_states):
            print("No tweets containing the keywords were found.")
            return []

        backend = Aer.get_backend('qasm_simulator')
        n = len(binary_states).bit_length()
        oracle = self.oracle_circuit(binary_states)
        grover_qc = self.grover_circuit(n, oracle)
        grover_qc.measure_all()
        job = backend.run(grover_qc, shots=1024)
        result = job.result()
        counts = result.get_counts()

        indices = [int(key, 2) for key, value in counts.items() if value > 0]
        valid_indices = sorted([index for index in indices if index < len(binary_states) and binary_states[index] == 1])
        return valid_indices

    def analyze_sentiment(self, tweet):
        """
        Analyze the sentiment of a single tweet.
        """
        score = self.sia.polarity_scores(tweet)
        return 'Positive' if score['compound'] >= 0 else 'Negative'

    def analyze_tweets_from_csv(self, csv_file, output_csv):
        """
        Analyze sentiments for tweets read from a CSV file and save results to a new file.
        """
        df = pd.read_csv(csv_file)

        if "Tweet" not in df.columns:
            raise ValueError("The input CSV file must contain a 'Tweet' column!")

        df["Sentiment"] = df["Tweet"].apply(self.analyze_sentiment)
        df.to_csv(output_csv, index=False)
        print(f"Analyzed tweets saved to {output_csv}")
        return df


# Save the GroverSentimentAnalyzer object to a pickle file
if __name__ == "__main__":
    analyzer = GroverSentimentAnalyzer()
    with open('grover_sentiment_analyzer.pkl', 'wb') as pkl_file:
        pickle.dump(analyzer, pkl_file)
    print("GroverSentimentAnalyzer object has been saved as grover_sentiment_analyzer.pkl")
