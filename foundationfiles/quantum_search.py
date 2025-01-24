import re
from nltk.corpus import stopwords
from nltk import download
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import pandas as pd
import csv


# List of Mental Health and Well-Being Keywords
mental_health_keywords = [
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

#preprocessing Twitter-tweets and encoding them to binary states
def preprocess_and_encode(tweets, keywords):
    stop_words = set(stopwords.words('english'))

    def clean_tweet(tweet):
        tweet = re.sub(r"http\S+", "", tweet)  # Remove URLs
        tweet = re.sub(r"[^a-zA-Z\s]", "", tweet)  # Remove special characters
        tweet = tweet.lower().strip()
        tweet = " ".join([word for word in tweet.split() if word not in stop_words])
        return tweet

    def contains_keyword(tweet, keywords):
        return any(keyword in tweet for keyword in keywords)

    binary_states = []
    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet)
        binary_states.append(1 if contains_keyword(cleaned_tweet, keywords) else 0)
    return binary_states

# Saving filtered data to csv
def save_to_csv(file_name, valid_indices, tweets):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Tweet"])  # Header
            for index in valid_indices:
                writer.writerow([index, tweets[index]])
        print(f"Target tweets successfully saved to {file_name}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

#defining Grover's Circuit
def grover_circuit(n, oracle):
    """
        n (int): Number of qubits (equal to log2 of number of items).
        oracle (QuantumCircuit): The oracle circuit.
    """
    qc = QuantumCircuit(n)
    #apply H-gates to all qubits
    qc.h(range(n))
    #applying Oracle
    qc.compose(oracle, inplace=True)  # Use compose instead of +=
    #diffusion Operator
    qc.h(range(n))
    qc.z(range(n))
    qc.cz(0, n - 1)  # Multi-controlled Z gate
    qc.h(range(n))    #returns the QuantumCircuit or grover's algorithm circuit.
    return qc

# Define Oracle Circuit
def oracle_circuit(binary_states):
    """
    Create the oracle circuit based on binary states.

    Args:
        binary_states (list): Binary encoding of tweets (1 for keyword presence, 0 otherwise).

    Returns:
        QuantumCircuit: The oracle circuit.
    """
    n = len(binary_states).bit_length()  # Number of qubits needed
    oracle = QuantumCircuit(n)
    for i, state in enumerate(binary_states):
        if state == 1:  # Only process states with 1
            binary_string = bin(i)[2:].zfill(n)
            for j, bit in enumerate(binary_string):
                if bit == '0':
                    oracle.x(j)  # Flip qubit for |0>
            oracle.mcx(list(range(n - 1)), n - 1)  # Multi-controlled Z
            for j, bit in enumerate(binary_string):
                if bit == '0':
                    oracle.x(j)  # Un-flip qubit
    return oracle

def grover_search(tweets):
    binary_states = preprocess_and_encode(tweets, mental_health_keywords)
    if not any(binary_states):
        print("No tweets containing the keywords were found.")
        return []

    backend = Aer.get_backend('qasm_simulator')
    n = len(binary_states).bit_length()
    oracle = oracle_circuit(binary_states)
    grover_qc = grover_circuit(n, oracle)
    grover_qc.measure_all()
    job = backend.run(grover_qc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    indices = [int(key, 2) for key, value in counts.items() if value > 0]
    valid_indices = sorted([index for index in indices if index < len(binary_states) and binary_states[index] == 1])
    return valid_indices

# Example Usage
if __name__ == "__main__":
    input_file = "tweet_data.csv"
    df = pd.read_csv(input_file)
    tweets = df['text'].tolist()  # Extract the text column


    valid_indices = grover_search(tweets)

    # Save target tweets to a CSV
    output_file = "target_tweets.csv"
    save_to_csv(output_file, valid_indices, tweets)
