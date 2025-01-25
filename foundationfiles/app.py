import streamlit as st
import pandas as pd
import subprocess
import os
from generic_nlp import GenericNLPAnalyzer  # Import Generic NLP Analyzer

# Initialize the Generic NLP Analyzer
analyzer = GenericNLPAnalyzer()

# ---- APP TITLE ----
st.set_page_config(page_title="Quansst", page_icon="✨", layout="wide")
st.title("✨ Quansst: AI-Powered Text Processing")
st.markdown(
    "Welcome to **Quansst**, an AI-driven platform that offers two powerful NLP-based functionalities:"
)
st.markdown(
    "- **Generic NLP Sentiment Analysis**: Perform sentiment analysis on general text data.\n"
    "- **Quantum Search & Sentiment Analysis**: Utilize quantum search to extract targeted tweets and analyze sentiment."
)

# ---- SIDEBAR MENU ----
st.sidebar.title("🔍 Select an NLP Task")
app_mode = st.sidebar.radio(
    "Choose a function:",
    ["Home", "Generic NLP Sentiment Analysis", "Quantum Search & Sentiment Analysis"]
)

# ---- HOME PAGE ----
if app_mode == "Home":
    st.header("Welcome to Quansst!")
    st.subheader("Choose an NLP task from the sidebar to get started.")
    st.image("quansst_banner.png", use_column_width=True)  # Optional: Add a banner image
    st.markdown(
        "🔹 **Generic NLP Sentiment Analysis:** Upload a CSV file with text data and analyze sentiment using the VADER model.\n"
        "🔹 **Quantum Search & Sentiment Analysis:** Perform Grover-based quantum search on tweets and analyze their sentiment."
    )
    st.info("Select an option from the sidebar to proceed.")

# ---- GENERIC NLP SENTIMENT ANALYSIS ----
elif app_mode == "Generic NLP Sentiment Analysis":
    st.header("📝 Generic NLP Sentiment Analysis")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file containing text data", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8", delimiter=",")

            if df.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            else:
                df = df.dropna(how="all")  # Remove empty rows
                df.columns = df.columns.str.strip()  # Remove extra spaces from column names

                if "text" not in df.columns:
                    st.error("The uploaded CSV file must contain a 'text' column.")
                else:
                    # Save uploaded file
                    input_csv = "uploaded_text_data.csv"
                    df.to_csv(input_csv, index=False)

                    # Process dataset with timing
                    with st.spinner("Processing..."):
                        result_df, execution_time = analyzer.process_dataset(input_csv)

                    if result_df is not None:
                        st.success(f"Processing Time: {execution_time:.2f} seconds")

                        # Display processed results
                        st.subheader("📊 Processed Data")
                        st.dataframe(result_df)

                        # Display sentiment distribution
                        st.subheader("📈 Sentiment Distribution")
                        sentiment_counts = result_df["Sentiment"].value_counts()
                        st.bar_chart(sentiment_counts)
                    else:
                        st.error("Error processing file. Please check the format and try again.")

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.warning("Please upload a CSV file.")

# ---- QUANTUM SEARCH & SENTIMENT ANALYSIS ----
elif app_mode == "Quantum Search & Sentiment Analysis":
    st.header("🔬 Quantum Search & Sentiment Analysis")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload a CSV file containing tweets", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            if "text" not in df.columns:
                st.error("The uploaded CSV file must contain a 'text' column.")
            else:
                input_csv = "tweet_data.csv"
                df.to_csv(input_csv, index=False)

                # Running Quantum Search
                with st.spinner("Running Quantum Search..."):
                    process = subprocess.run(["python", "quantum_search.py"], capture_output=True, text=True)
                    quantum_output = process.stdout.strip()
                    st.text_area("Quantum Search Output:", quantum_output or "No output received.")

                # Check if target tweets exist before sentiment analysis
                target_csv = "target_tweets.csv"
                if os.path.exists(target_csv) and os.path.getsize(target_csv) > 0:
                    with st.spinner("Performing Sentiment Analysis..."):
                        process = subprocess.run(["python", "sentiment_analysis.py"], capture_output=True, text=True)
                        sentiment_output = process.stdout.strip()
                        st.text_area("Sentiment Analysis Output:", sentiment_output or "No output received.")

                    # Display Results
                    output_csv = "analyzed_tweets.csv"
                    if os.path.exists(output_csv) and os.path.getsize(output_csv) > 0:
                        result_df = pd.read_csv(output_csv)

                        st.subheader("📊 Results")
                        st.dataframe(result_df)

                        # Sentiment Distribution Chart
                        st.subheader("📈 Sentiment Distribution")
                        sentiment_counts = result_df["Sentiment"].value_counts()
                        st.bar_chart(sentiment_counts)
                    else:
                        st.warning("No analyzed tweets found. Ensure sentiment analysis ran correctly.")

                else:
                    st.warning("No target tweets found for sentiment analysis.")

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.warning("Please upload a CSV file.")
