# import dash
# from dash import dcc, html, Input, Output, State
# import pandas as pd
# import plotly.express as px
# from collections import Counter
# from textblob import TextBlob
# import io
# import base64

# # Initialize the Dash app
# app = dash.Dash(__name__)

# # App Layout
# app.layout = html.Div([
#     html.H1("Text Analysis Dashboard", style={"textAlign": "center"}),
    
#     # File Upload Section
#     html.Div([
#         html.H3("Upload a CSV or Excel File:"),
#         dcc.Upload(
#             id="upload-data",
#             children=html.Div(["Drag and Drop or Click to Upload"]),
#             style={
#                 "width": "100%",
#                 "height": "60px",
#                 "lineHeight": "60px",
#                 "borderWidth": "1px",
#                 "borderStyle": "dashed",
#                 "borderRadius": "5px",
#                 "textAlign": "center",
#                 "marginBottom": "10px"
#             },
#             multiple=False
#         )
#     ]),
    
#     # Output for Charts
#     html.Div(id="output-charts")
# ])

# # Helper Function: Process Text Data
# def process_text(data):
#     all_words = " ".join(data).split()
#     word_counts = Counter(all_words).most_common(10)  # Top 10 words
#     words_df = pd.DataFrame(word_counts, columns=["Word", "Count"])
    
#     # Sentiment Analysis
#     sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
#     for text in data:
#         sentiment = TextBlob(text).sentiment.polarity
#         if sentiment > 0:
#             sentiments["Positive"] += 1
#         else sentiment < 0:
#             sentiments["Negative"] += 1
            
#     sentiment_df = pd.DataFrame(sentiments.items(), columns=["Sentiment", "Count"])
    
#     return words_df, sentiment_df

# # Callback to Handle File Upload and Generate Charts
# @app.callback(
#     Output("output-charts", "children"),
#     Input("upload-data", "contents"),
#     State("upload-data", "filename"),
# )
# def update_output(contents, filename):
#     if contents is None:
#         return html.Div("No file uploaded yet.")
    
#     # Parse the uploaded file
#     content_type, content_string = contents.split(",")
#     decoded = io.BytesIO(base64.b64decode(content_string))
    
#     try:
#         if filename.endswith(".csv"):
#             df = pd.read_csv(decoded)
#         elif filename.endswith(".xlsx"):
#             df = pd.read_excel(decoded)
#         else:
#             return html.Div("Unsupported file format. Please upload a CSV or Excel file.")
#     except Exception as e:
#         return html.Div(f"Error reading file: {e}")
    
#     # Assuming a column named 'Tweet' contains the textual data
#     if "Tweet" not in df.columns:
#         return html.Div("The file must contain a 'Tweet' column.")
    
#     # Process Text Data
#     words_df, sentiment_df = process_text(df["Tweet"].astype(str))
    
#     # Create Bar Chart for Word Counts
#     word_chart = px.bar(words_df, x="Word", y="Count", title="Top 10 Words", text="Count")
    
#     # Create Pie Chart for Sentiments
#     sentiment_chart = px.pie(sentiment_df, names="Sentiment", values="Count", title="Sentiment Analysis")
    
#     return html.Div([
#         dcc.Graph(figure=word_chart),
#         dcc.Graph(figure=sentiment_chart)
#     ])

# # Run the app
# if __name__ == "__main__":
#     app.run_server(debug=True)


import backend.dash_app as dash_app
from backend.dash_app import dcc, html
import requests
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import pandas as pd

# Initialize Dash app
app = dash_app.Dash(__name__)
app.title = "Sentiment Analysis Dashboard"

app.layout = html.Div([
    html.H1("Sentiment Analysis Dashboard"),
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload CSV"),
        multiple=False
    ),
    html.Div(id="output-data"),
    html.Div(id="charts"),
])


@app.callback(
    [dash_app.dependencies.Output("output-data", "children"),
     dash_app.dependencies.Output("charts", "children")],
    [dash_app.dependencies.Input("upload-data", "contents")],
    [dash_app.dependencies.State("upload-data", "filename")]
)
def update_output(contents, filename):
    if contents is None:
        return "Please upload a file.", []

    # Extract content and send to backend
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    files = {"file": (filename, decoded)}

    # Send file to Flask backend
    response = requests.post("http://127.0.0.1:5000/process", files=files)
    if response.status_code != 200:
        return f"Error: {response.json().get('error', 'Unknown error')}", []

    data = response.json()

    # Time Comparison Chart
    time_df = pd.DataFrame({
        "Algorithm": ["Grover", "Generic NLP"],
        "Time (seconds)": [data["grover_time"], data["generic_time"]]
    })
    time_fig = px.bar(time_df, x="Algorithm", y="Time (seconds)", title="Processing Time Comparison")

    # Sentiment Distribution Chart
    sentiment_df = pd.DataFrame({
        "Sentiment": ["Positive", "Negative"],
        "Grover": [data["grover_sentiments"].get("Positive", 0), data["grover_sentiments"].get("Negative", 0)],
        "Generic NLP": [data["generic_sentiments"].get("Positive", 0), data["generic_sentiments"].get("Negative", 0)]
    })
    sentiment_fig = px.bar(
        sentiment_df.melt(id_vars="Sentiment", var_name="Algorithm", value_name="Count"),
        x="Sentiment", y="Count", color="Algorithm", barmode="group",
        title="Sentiment Distribution Comparison"
    )

    # Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(data["word_counts"])
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    buffer.seek(0)
    wordcloud_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return (
        f"File '{filename}' processed successfully!",
        [
            dcc.Graph(figure=time_fig),
            dcc.Graph(figure=sentiment_fig),
            html.Div([
                html.H3("Word Cloud"),
                html.Img(src=f"data:image/png;base64,{wordcloud_base64}")
            ])
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
