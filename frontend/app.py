from flask import Flask, render_template, request
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and generate insights
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process CSV
        df = pd.read_csv(file_path)
        text_data = ' '.join(df.iloc[:, 0].astype(str))  # Combine all text from the first column

        # Generate WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        wordcloud_path = os.path.join('static', 'wordcloud.png')
        wordcloud.to_file(wordcloud_path)

        # Word Frequency Bar Chart
        words = text_data.split()
        word_freq = pd.Series(words).value_counts().head(10)
        freq_fig = px.bar(
            x=word_freq.index, y=word_freq.values,
            labels={'x': 'Words', 'y': 'Frequency'},
            title='Top 10 Frequent Words'
        )
        freq_chart_path = os.path.join('static', 'word_freq.html')
        freq_fig.write_html(freq_chart_path)

        return render_template(
            'results.html',
            wordcloud_path=wordcloud_path,
            freq_chart_path=freq_chart_path
        )

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
