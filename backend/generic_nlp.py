# import time
# import pandas as pd
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk import download

# # Download VADER lexicon
# download("vader_lexicon")

# # Initialize VADER
# sia = SentimentIntensityAnalyzer()

# # Load dataset
# file_name = "tweet_data.csv"
# df = pd.read_csv(file_name)

# # Preprocessing Function
# def preprocess_text(text):
#     return text.lower().strip()  # Basic preprocessing (lowercasing)

# # Analyze Sentiment with VADER
# def analyze_sentiment_vader(text):
#     score = sia.polarity_scores(text)
#     return 'Positive' if score['compound'] >= 0 else 'Negative'

# # Generic NLP Pipeline
# start_time = time.time()
# df['cleaned_text'] = df['text'].apply(preprocess_text)
# df['Sentiment'] = df['cleaned_text'].apply(analyze_sentiment_vader)
# end_time = time.time()

# print(f"Generic NLP Pipeline Time: {end_time - start_time:.2f} seconds")
# print(f"Processed {len(df)} tweets.")


import time
import pickle
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
        return text.lower().strip()

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
        df = pd.read_csv(file_name)

        # Start timing
        start_time = time.time()

        # Preprocessing and sentiment analysis
        df['cleaned_text'] = df['text'].apply(self.preprocess_text)
        df['Sentiment'] = df['cleaned_text'].apply(self.analyze_sentiment_vader)

        # End timing
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Generic NLP Pipeline Time: {execution_time:.2f} seconds")
        print(f"Processed {len(df)} tweets.")

        # Return processed DataFrame and execution time
        return df, execution_time


# Save the GenericNLPAnalyzer object to a pickle file
if __name__ == "__main__":
    analyzer = GenericNLPAnalyzer()
    with open('generic_nlp_analyzer.pkl', 'wb') as pkl_file:
        pickle.dump(analyzer, pkl_file)
    print("GenericNLPAnalyzer object has been saved as generic_nlp_analyzer.pkl")
