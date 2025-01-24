import time
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download

# Download VADER lexicon
download("vader_lexicon")

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Load dataset
file_name = "tweet_data.csv"
df = pd.read_csv(file_name)

# Preprocessing Function
def preprocess_text(text):
    return text.lower().strip()  # Basic preprocessing (lowercasing)

# Analyze Sentiment with VADER
def analyze_sentiment_vader(text):
    score = sia.polarity_scores(text)
    return 'Positive' if score['compound'] >= 0 else 'Negative'

# Generic NLP Pipeline
start_time = time.time()
df['cleaned_text'] = df['text'].apply(preprocess_text)
df['Sentiment'] = df['cleaned_text'].apply(analyze_sentiment_vader)
end_time = time.time()

print(f"Generic NLP Pipeline Time: {end_time - start_time:.2f} seconds")
print(f"Processed {len(df)} tweets.")
