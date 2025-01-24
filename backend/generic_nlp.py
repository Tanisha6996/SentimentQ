import time
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords
from nltk import download

# Download stopwords
download('stopwords')

# Load Dataset (Replace 'your_dataset.csv' with your file)
file_name = "tweet_data.csv"
df = pd.read_csv(file_name)

# Check the size of the dataset
print(f"Dataset contains {len(df)} rows")

# Preprocessing Function
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = text.lower().strip()  # Convert to lowercase
    text = " ".join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text

# Apply preprocessing to text column
print("Preprocessing data...")
start_preprocessing = time.time()  # Timer start for preprocessing
df['cleaned_text'] = df['text'].apply(preprocess_text)
end_preprocessing = time.time()  # Timer end for preprocessing
print(f"Preprocessing completed in {end_preprocessing - start_preprocessing:.2f} seconds")

# Split Data into Train and Test
X = df['cleaned_text']  # Features
y = df['sentiment']  # Labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization
print("Vectorizing text data using TF-IDF...")
start_vectorizing = time.time()  # Timer start for vectorization
vectorizer = TfidfVectorizer(max_features=10000)  # Limit to 10,000 features for efficiency
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
end_vectorizing = time.time()  # Timer end for vectorization
print(f"Vectorization completed in {end_vectorizing - start_vectorizing:.2f} seconds")

# Train Naive Bayes Classifier
print("Training the Naive Bayes Classifier...")
start_training = time.time()  # Timer start for training
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)
end_training = time.time()  # Timer end for training
print(f"Training completed in {end_training - start_training:.2f} seconds")

# Make Predictions
print("Making predictions on test data...")
start_prediction = time.time()  # Timer start for prediction
y_pred = model.predict(X_test_tfidf)
end_prediction = time.time()  # Timer end for prediction
print(f"Prediction completed in {end_prediction - start_prediction:.2f} seconds")

# Evaluate the Model
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Overall Timer
overall_time = (
    (end_preprocessing - start_preprocessing) +
    (end_vectorizing - start_vectorizing) +
    (end_training - start_training) +
    (end_prediction - start_prediction)
)
print(f"\nOverall model processing time: {overall_time:.2f} seconds")

# Example Predictions
print("\nExample Predictions:")
examples = ["I love this product!", "This is the worst experience ever."]
examples_tfidf = vectorizer.transform([preprocess_text(text) for text in examples])
predictions = model.predict(examples_tfidf)
for text, sentiment in zip(examples, predictions):
    print(f"Text: {text} | Predicted Sentiment: {sentiment}")
