import time
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download

# Download VADER lexicon
download("vader_lexicon")

class GenericNLPAnalyzer:
    def __init__(self):
        # Initialize VADER sentiment analyzer
        self.sia = SentimentIntensityAnalyzer()

    @staticmethod
    def preprocess_text(text):
        """
        Basic text preprocessing: lowercasing and stripping whitespace.
        """
        return str(text).lower().strip()

    def analyze_sentiment_vader(self, text):
        """
        Analyze sentiment using VADER.
        Returns 'Positive' for compound >= 0, otherwise 'Negative'.
        """
        score = self.sia.polarity_scores(text)
        return 'Positive' if score['compound'] >= 0 else 'Negative'

    def process_dataset(self, file_name):
        """
        Load a dataset, preprocess text, and analyze sentiment.
        Measures execution time for the entire pipeline.
        """
        try:
            df = pd.read_csv(file_name, encoding="utf-8", delimiter=",")  # Read CSV properly

            if df.empty:
                raise ValueError("The uploaded file is empty.")

            df = df.dropna(how="all")  # Remove completely empty rows
            df.columns = df.columns.str.strip()  # Strip extra spaces from column names

            if "text" not in df.columns:
                raise ValueError("The uploaded CSV file must contain a 'text' column.")

            # Start timing
            start_time = time.time()

            # Preprocessing and sentiment analysis
            df["cleaned_text"] = df["text"].apply(self.preprocess_text)
            df["Sentiment"] = df["cleaned_text"].apply(self.analyze_sentiment_vader)

            # End timing
            end_time = time.time()
            execution_time = end_time - start_time

            print(f"Generic NLP Pipeline Time: {execution_time:.2f} seconds")
            print(f"Processed {len(df)} tweets.")

            return df, execution_time  # Return processed data and execution time

        except Exception as e:
            print(f"Error processing dataset: {e}")
            return None, None
