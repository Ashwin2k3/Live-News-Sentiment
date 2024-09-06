import streamlit as st
import requests
import csv
import time
from textblob import TextBlob
import threading

# Load company data from CSV (global dataset)
def load_company_data(file_path='stock.csv'):
    company_data = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row['Symbol'].strip().upper()
                company_data[ticker] = row['Name']
    except Exception as e:
        st.error(f"Error loading company data: {e}")
    return company_data

# Function to fetch news articles from the News API
def fetch_news(query, language='en', num_articles=10):
    api_key = "7c9628099fbd4d63be8c502113ad9ec7"  # Your News API key
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}&pageSize={num_articles}"
    try:
        response = requests.get(url, timeout=10)  # Add timeout to prevent hanging
        response.raise_for_status()  # Check for request errors
        news_data = response.json()
        return news_data.get('articles', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

# Initialize the sentiment analysis pipeline
def initialize_sentiment_pipeline():
    return TextBlob

# Analyze sentiments of fetched texts
def analyze_sentiments(sentiment_pipeline, texts):
    if sentiment_pipeline:
        try:
            return [sentiment_pipeline(text) for text in texts]
        except Exception as e:
            st.error(f"Error during sentiment analysis: {e}")
            return []
    else:
        return []

# Determine market signal based on sentiment analysis results
def get_signal_from_sentiments(sentiments):
    positive_count = sum(1 for sentiment in sentiments if sentiment.polarity > 0)
    negative_count = sum(1 for sentiment in sentiments if sentiment.polarity < 0)
    
    if positive_count > negative_count:
        return "Buy"
    elif negative_count > positive_count:
        return "Sell"
    else:
        return "Hold"

# Function to fetch and display news and sentiment analysis
def fetch_and_display_news(stock_ticker, company_data):
    sentiment_pipeline = initialize_sentiment_pipeline()
    
    query = company_data.get(stock_ticker, stock_ticker)
    articles = fetch_news(query, num_articles=10)

    if articles:
        texts = [article['description'] for article in articles if article['description']]
        if texts:
            sentiments = analyze_sentiments(sentiment_pipeline, texts)
            
            # Determine the new signal
            new_signal = get_signal_from_sentiments(sentiments)
            
            # Display the current sentiment signal
            st.subheader("Current Sentiment Signal")
            st.write(f"The current sentiment signal for {stock_ticker} is: **{new_signal}**")
            
            st.subheader("News Articles")
            for i, article in enumerate(articles):
                st.write(f"**Title**: {article['title']}")
                st.write(f"**Description**: {article['description']}")
                if i < len(sentiments):
                    sentiment = sentiments[i]
                    polarity = sentiment.polarity
                    sentiment_label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
                    st.write(f"**Sentiment**: {sentiment_label} (Polarity: {polarity:.2f})")
                else:
                    st.write("**Sentiment**: Not available")
                st.write("---")
        else:
            st.write("No descriptions found in the articles to analyze.")
    else:
        st.write("No articles found.")

# Function to continuously fetch and display news
def continuous_news_fetching(stock_ticker, company_data, interval):
    while True:
        with st.spinner("Fetching and analyzing news articles..."):
            fetch_and_display_news(stock_ticker, company_data)
        time.sleep(interval)

# Main function to show sentiment analysis and start monitoring
def show_sentiment_analysis():
    st.title("Live Stock Market News Sentiment Monitoring")

    # Load company data from CSV
    company_data = load_company_data()

    # Dropdown to select the stock ticker
    stock_ticker = st.selectbox("Select stock ticker to monitor:", options=list(company_data.keys()))

    # Set the interval for fetching news (e.g., every 60 seconds)
    interval = st.slider("Select refresh interval (seconds):", 10, 300, 60)

    if stock_ticker:
        # Start the continuous news fetching in a separate thread
        threading.Thread(target=continuous_news_fetching, args=(stock_ticker, company_data, interval), daemon=True).start()

# Run the Streamlit app
show_sentiment_analysis()

# import streamlit as st
# import requests
# import csv
# import time
# from textblob import TextBlob

# # Load company data from CSV (global dataset)
# def load_company_data(file_path='stock.csv'):
#     company_data = {}
#     try:
#         with open(file_path, mode='r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 ticker = row['Symbol'].strip().upper()
#                 company_data[ticker] = row['Name']
#     except Exception as e:
#         st.error(f"Error loading company data: {e}")
#     return company_data

# # Function to fetch news articles from the News API
# def fetch_news(query, language='en', num_articles=10):
#     api_key = "YOUR_NEWS_API_KEY"  # Replace with your News API key
#     url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}&pageSize={num_articles}"
#     try:
#         response = requests.get(url, timeout=10)  # Add timeout to prevent hanging
#         response.raise_for_status()  # Check for request errors
#         news_data = response.json()
#         return news_data.get('articles', [])
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching news: {e}")
#         return []

# # Initialize the sentiment analysis pipeline
# def initialize_sentiment_pipeline():
#     return TextBlob

# # Analyze sentiments of fetched texts
# def analyze_sentiments(sentiment_pipeline, texts):
#     if sentiment_pipeline:
#         try:
#             return [sentiment_pipeline(text) for text in texts]
#         except Exception as e:
#             st.error(f"Error during sentiment analysis: {e}")
#             return []
#     else:
#         return []

# # Determine market signal based on sentiment analysis results
# def get_signal_from_sentiments(sentiments):
#     positive_count = sum(1 for sentiment in sentiments if sentiment.polarity > 0)
#     negative_count = sum(1 for sentiment in sentiments if sentiment.polarity < 0)
    
#     if positive_count > negative_count:
#         return "Buy"
#     elif negative_count > positive_count:
#         return "Sell"
#     else:
#         return "Hold"

# # Function to fetch and display news and sentiment analysis
# def display_news_and_sentiments(stock_ticker, company_data):
#     sentiment_pipeline = initialize_sentiment_pipeline()
    
#     st.write(f"Fetching news articles for {stock_ticker}...")
#     query = company_data.get(stock_ticker, stock_ticker)
#     articles = fetch_news(query, num_articles=10)

#     if articles:
#         texts = [article['description'] for article in articles if article['description']]
#         if texts:
#             sentiments = analyze_sentiments(sentiment_pipeline, texts)
            
#             # Determine the new signal
#             new_signal = get_signal_from_sentiments(sentiments)
            
#             # Display the current sentiment signal
#             st.subheader("Current Sentiment Signal")
#             st.write(f"The current sentiment signal for {stock_ticker} is: **{new_signal}**")
            
#             st.subheader("News Articles")
#             for i, article in enumerate(articles):
#                 st.write(f"**Title**: {article['title']}")
#                 st.write(f"**Description**: {article['description']}")
#                 if i < len(sentiments):
#                     sentiment = sentiments[i]
#                     polarity = sentiment.polarity
#                     sentiment_label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
#                     st.write(f"**Sentiment**: {sentiment_label} (Polarity: {polarity:.2f})")
#                 else:
#                     st.write("**Sentiment**: Not available")
#                 st.write("---")
#         else:
#             st.write("No descriptions found in the articles to analyze.")
#     else:
#         st.write("No articles found.")

# # Main function to show sentiment analysis and start monitoring
# def show_sentiment_analysis():
#     st.title("Live Stock Market News Sentiment Monitoring")

#     # Load company data from CSV
#     company_data = load_company_data()

#     # Dropdown to select the stock ticker
#     stock_ticker = st.selectbox("Select stock ticker to monitor:", options=list(company_data.keys()))

#     if stock_ticker:
#         display_news_and_sentiments(stock_ticker, company_data)

#     # Automatically refresh the page every 60 seconds
#     st.experimental_rerun()

# # Run the Streamlit app
# show_sentiment_analysis()
