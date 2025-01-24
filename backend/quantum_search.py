# import re
# from nltk.corpus import stopwords
# from nltk import download
# from qiskit import QuantumCircuit
# from qiskit_aer import Aer
# from qiskit.visualization import plot_histogram
# import csv

# # Download stopwords
# download('stopwords')

# # List of Mental Health and Well-Being Keywords
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

# # Preprocess Tweets and Encode Binary States
# def preprocess_and_encode(tweets, keywords):
#     """
#     Preprocess tweets and encode binary states for Grover's Algorithm.

#     Args:
#         tweets (list): List of tweet texts.
#         keywords (list): List of mental health-related keywords.

#     Returns:
#         list: Binary encoding for tweets (1 if a keyword is present, 0 otherwise).
#     """
#     stop_words = set(stopwords.words('english'))

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

# # Save Target Tweets to CSV
# def save_to_csv(file_name, valid_indices, tweets):
#     try:
#         with open(file_name, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Index", "Tweet"])  # Header
#             for index in valid_indices:
#                 writer.writerow([index, tweets[index]])
#         print(f"Target tweets successfully saved to {file_name}")
#     except Exception as e:
#         print(f"Error saving to CSV: {e}")

# # Define Grover's Circuit
# def grover_circuit(n, oracle):
#     """
#     Construct Grover's Algorithm circuit.

#     Args:
#         n (int): Number of qubits (equal to log2 of number of items).
#         oracle (QuantumCircuit): The oracle circuit.

#     Returns:
#         QuantumCircuit: Grover's Algorithm circuit.
#     """
#     qc = QuantumCircuit(n)
#     # Step 1: Apply H-gates to all qubits
#     qc.h(range(n))
#     # Step 2: Apply Oracle
#     qc.compose(oracle, inplace=True)  # Use compose instead of +=
#     # Step 3: Diffusion Operator
#     qc.h(range(n))
#     qc.z(range(n))
#     qc.cz(0, n - 1)  # Multi-controlled Z gate
#     qc.h(range(n))
#     return qc


# # Define Oracle Circuit
# def oracle_circuit(binary_states):
#     """
#     Create the oracle circuit based on binary states.

#     Args:
#         binary_states (list): Binary encoding of tweets (1 for keyword presence, 0 otherwise).

#     Returns:
#         QuantumCircuit: The oracle circuit.
#     """
#     n = len(binary_states).bit_length()  # Number of qubits needed
#     oracle = QuantumCircuit(n)
#     for i, state in enumerate(binary_states):
#         if state == 1:  # Only process states with 1
#             binary_string = bin(i)[2:].zfill(n)
#             for j, bit in enumerate(binary_string):
#                 if bit == '0':
#                     oracle.x(j)  # Flip qubit for |0>
#             oracle.mcx(list(range(n - 1)), n - 1)  # Multi-controlled Z
#             for j, bit in enumerate(binary_string):
#                 if bit == '0':
#                     oracle.x(j)  # Un-flip qubit
#     return oracle

# def grover_search(tweets):
#     """
#     Run Grover's Algorithm to find tweets containing mental health-related keywords.

#     Args:
#         tweets (list): List of tweet texts.

#     Returns:
#         list: Indices of tweets containing keywords.
#     """
#     print("Preprocessing tweets...")
#     binary_states = preprocess_and_encode(tweets, mental_health_keywords)

#     if not any(binary_states):
#         print("No tweets containing the keywords were found.")
#         return []

#     print(f"Binary States: {binary_states}")

#     # Define oracle and Grover's circuit
#     oracle = oracle_circuit(binary_states)
#     n = len(binary_states).bit_length()
#     assert 2 ** n >= len(binary_states), "Number of qubits is insufficient for binary encoding."

#     grover_qc = grover_circuit(n, oracle)

#     # Simulate Grover's Algorithm
#     backend = Aer.get_backend('qasm_simulator')
#     grover_qc.measure_all()
#     job = backend.run(grover_qc,shots=1024)
#     result = job.result()
#     counts = result.get_counts()


#     # Find the most likely indices
#     indices = [int(key, 2) for key, value in counts.items() if value > 0]
#     valid_indices = sorted([index for index in indices if index < len(binary_states) and binary_states[index] == 1])  # Only keep indices with binary_state=1

#     # # Debug print to verify mapping
#     # print("\nMapping Indices to Tweets:")
#     # for index in valid_indices:
#     #     print(f"Index {index}: {tweets[index]}")

#     return valid_indices


# # Example Usage
# if __name__ == "__main__":
#     # Example list of tweets
#     tweets = [
#         "Stress is a big part of my life right now.",
#         "I love practicing mindfulness every morning.",
#         "Work deadlines are killing me! Need some relaxation.",
#         "Mental health is just as important as physical health.",
#         "I started journaling, and it has helped me manage anxiety.",
#         "Burnout is real. Take care of yourself!",
#         "Gratitude journaling is the best self-care practice.",
#         "Feeling calm and positive after my therapy session.",
#         "Insomnia is making my days so stressful.",
#         "Donald Trump is the president of India."
#     ]

#     # Output Target Tweets
#     print("\nTarget Tweets:")
#     valid_indices = grover_search(tweets)  # Call the updated function
#     for index in valid_indices:
#         print(f"{index}: {tweets[index]}")


#     output_file = "target_tweets.csv"
#     valid_indices = grover_search(tweets)
#     save_to_csv(output_file, valid_indices, tweets)

import re
from nltk.corpus import stopwords
from nltk import download
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import pandas as pd
import csv

# Download stopwords
download('stopwords')

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

# Preprocess Tweets and Encode Binary States
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

# Save Target Tweets to CSV
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

# Define Grover's Circuit
def grover_circuit(n, oracle):
    """
    Construct Grover's Algorithm circuit.

    Args:
        n (int): Number of qubits (equal to log2 of number of items).
        oracle (QuantumCircuit): The oracle circuit.

    Returns:
        QuantumCircuit: Grover's Algorithm circuit.
    """
    qc = QuantumCircuit(n)
    # Step 1: Apply H-gates to all qubits
    qc.h(range(n))
    # Step 2: Apply Oracle
    qc.compose(oracle, inplace=True)  # Use compose instead of +=
    # Step 3: Diffusion Operator
    qc.h(range(n))
    qc.z(range(n))
    qc.cz(0, n - 1)  # Multi-controlled Z gate
    qc.h(range(n))
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

    print(f"Binary States: {binary_states}")

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
