import streamlit as st
import pandas as pd
import os
from generic_nlp import GenericNLPAnalyzer

# Initialize analyzer
analyzer = GenericNLPAnalyzer()

st.title("Generic NLP Sentiment Analysis")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file containing text data", type=["csv"])

if uploaded_file:
    try:
        # Read CSV file
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
                    st.subheader("Processed Data")
                    st.dataframe(result_df)

                    # Display sentiment distribution
                    st.subheader("Sentiment Distribution")
                    sentiment_counts = result_df["Sentiment"].value_counts()
                    st.bar_chart(sentiment_counts)
                else:
                    st.error("Error processing file. Please check the format and try again.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a CSV file.")
