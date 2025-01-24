from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

app = Flask(__name__)

# Route to Upload CSV and Generate Charts
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file is uploaded
        if "file" not in request.files:
            return "No file uploaded!", 400

        file = request.files["file"]

        # Load the uploaded CSV file
        df = pd.read_csv(file)

        # Ensure required columns exist
        if "Sentiment" not in df.columns:
            return "The uploaded file must contain a 'Sentiment' column!", 400

        # Generate Sentiment Distribution Chart
        sentiment_chart_path = generate_sentiment_distribution_chart(df)

        # Generate Word Cloud
        wordcloud_path = generate_wordcloud(df)

        return render_template(
            "charts.html",
            sentiment_chart=sentiment_chart_path,
            wordcloud=wordcloud_path,
        )

    return render_template("upload.html")


def generate_sentiment_distribution_chart(df):
    """
    Generate a bar chart showing sentiment distribution.

    Args:
        df (DataFrame): DataFrame containing a 'Sentiment' column.

    Returns:
        str: Path to the saved chart image.
    """
    sentiment_counts = df["Sentiment"].value_counts()
    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind="bar", color=["green", "red"], alpha=0.7)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the chart as an image
    chart_path = "static/sentiment_distribution.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path


def generate_wordcloud(df):
    """
    Generate a word cloud for the 'Tweet' column.

    Args:
        df (DataFrame): DataFrame containing a 'Tweet' column.

    Returns:
        str: Path to the saved word cloud image.
    """
    if "Tweet" not in df.columns:
        return None

    # Combine all tweets into one string
    text = " ".join(df["Tweet"].dropna().astype(str))

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Tweets")
    plt.tight_layout()

    # Save the word cloud as an image
    wordcloud_path = "static/wordcloud.png"
    plt.savefig(wordcloud_path)
    plt.close()

    return wordcloud_path


if __name__ == "__main__":
    app.run(debug=True)
