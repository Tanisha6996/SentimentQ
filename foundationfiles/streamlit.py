import streamlit as st
import pandas as pd
import subprocess
import os

st.title("Quantum Search & Sentiment Analysis")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file containing tweets", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)  # Read CSV file
        
        if "text" not in df.columns:
            st.error("The uploaded CSV file must contain a 'text' column.")
        else:
            input_csv = "tweet_data.csv"  # Save input data
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

                    st.subheader("Results")
                    st.dataframe(result_df)

                    # Sentiment Distribution Chart
                    st.subheader("Sentiment Distribution")
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
