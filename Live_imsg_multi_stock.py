# import streamlit as st
# import requests
# import csv
# import time
# from textblob import TextBlob
# import subprocess
# from concurrent.futures import ThreadPoolExecutor

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
# def fetch_news(query, num_articles=10, language='en'):
#     api_key = "7c9628099fbd4d63be8c502113ad9ec7"  # Your News API key
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

# # Send iMessage notification when signal changes
# def send_imessage(recipient, message):
#     script = f"""
#     tell application "Messages"
#         set targetBuddy to "{recipient}"
#         set targetService to 1 -- 1 is the iMessage service
#         set theMessage to "{message}"
#         send theMessage to buddy targetBuddy of service targetService
#     end tell
#     """
#     try:
#         subprocess.run(["osascript", "-e", script], check=True)
#         st.success(f"iMessage sent to {recipient}!")
#     except subprocess.CalledProcessError as e:
#         st.error(f"Error sending iMessage: {e}")

# # Function to monitor sentiment for a single stock and send notifications
# def monitor_single_stock(stock_ticker, company_data, recipient, num_articles, check_interval=60):
#     sentiment_pipeline = initialize_sentiment_pipeline()
#     last_signal = None
#     news_placeholder = st.empty()  # Placeholder for live news updates

#     while True:
#         with st.spinner(f"Fetching and analyzing news articles for {stock_ticker}..."):
#             query = company_data.get(stock_ticker, stock_ticker)
#             articles = fetch_news(query, num_articles=num_articles)

#         if articles:
#             news_content = ""
#             texts = [article['description'] for article in articles if article['description']]
#             if texts:
#                 sentiments = analyze_sentiments(sentiment_pipeline, texts)

#                 # Determine the new signal
#                 new_signal = get_signal_from_sentiments(sentiments)

#                 # Check if the signal has changed
#                 if new_signal != last_signal:
#                     st.write(f"Sentiment signal for {stock_ticker} changed to: **{new_signal}**")
#                     send_imessage(recipient, f"The sentiment signal for {stock_ticker} has changed to {new_signal}.")
#                     last_signal = new_signal
#                 else:
#                     st.write(f"No change in sentiment signal for {stock_ticker}. Current signal: **{new_signal}**")

#                 # Update news content with dividers between articles
#                 for article in articles:
#                     title = article.get('title', 'No title')
#                     description = article.get('description', 'No description')
#                     news_content += f"**{title}**\n{description}\n\n"
#                     news_content += "---\n"  # Add a divider after each article

#             else:
#                 news_content = f"No descriptions found in the articles for {stock_ticker} to analyze."
#         else:
#             news_content = f"No articles found for {stock_ticker}."

#         # Display the updated news with dividers
#         news_placeholder.markdown(f"### {stock_ticker} News\n" + news_content)

#         # Wait for the specified interval before checking again
#         time.sleep(check_interval)

# # Function to monitor sentiment for multiple stocks
# def monitor_multiple_stocks(stock_tickers, company_data, recipient, num_articles, check_interval=60):
#     # Use a ThreadPoolExecutor to run sentiment monitoring for each stock in parallel
#     with ThreadPoolExecutor() as executor:
#         for stock_ticker in stock_tickers:
#             executor.submit(monitor_single_stock, stock_ticker, company_data, recipient, num_articles, check_interval)

# # Main function to show sentiment analysis and start monitoring
# def show_sentiment_analysis():
#     st.title("Live Stock Market News Sentiment Monitoring")

#     # Load company data from CSV
#     company_data = load_company_data()

#     # Multi-select box to select stock tickers
#     stock_tickers = st.multiselect("Select stock tickers to monitor:", options=list(company_data.keys()))

#     # Input to select number of news articles to fetch
#     num_articles = st.slider("Select the number of news articles to fetch for each stock:", min_value=1, max_value=20, value=10)

#     # Input phone number for iMessage notifications
#     recipient = st.text_input("Enter phone number to receive iMessage notifications (format: +1234567890):", value="+918287936541")

#     # Interval to refresh and monitor news (in seconds)
#     check_interval = st.slider("Set the time interval (seconds) between each sentiment check:", min_value=30, max_value=600, value=60)

#     if st.button("Start Monitoring"):
#         if stock_tickers:
#             monitor_multiple_stocks(stock_tickers, company_data, recipient, num_articles, check_interval)
#         else:
#             st.error("Please select at least one stock ticker to monitor.")

# # Run the Streamlit app
# show_sentiment_analysis()

import streamlit as st
import requests
import csv
import time
from textblob import TextBlob
import subprocess
from concurrent.futures import ThreadPoolExecutor

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
def fetch_news(query, num_articles=10, language='en'):
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

# Send iMessage notification when signal changes
def send_imessage(recipient, message):
    script = f"""
    tell application "Messages"
        set targetBuddy to "{recipient}"
        set targetService to 1 -- 1 is the iMessage service
        set theMessage to "{message}"
        send theMessage to buddy targetBuddy of service targetService
    end tell
    """
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        st.success(f"iMessage sent to {recipient}!")
    except subprocess.CalledProcessError as e:
        st.error(f"Error sending iMessage: {e}")

# Function to display and monitor sentiment for a single stock and send notifications
def monitor_single_stock(stock_ticker, company_data, recipient, num_articles, check_interval=60):
    sentiment_pipeline = initialize_sentiment_pipeline()
    last_signal = None
    news_placeholder = st.empty()  # Placeholder for live news updates

    while True:
        with st.spinner(f"Fetching and analyzing news articles for {stock_ticker}..."):
            query = company_data.get(stock_ticker, stock_ticker)
            articles = fetch_news(query, num_articles=num_articles)

        if articles:
            news_content = ""
            texts = [article['description'] for article in articles if article['description']]
            if texts:
                sentiments = analyze_sentiments(sentiment_pipeline, texts)

                # Determine the new signal
                new_signal = get_signal_from_sentiments(sentiments)

                # Check if the signal has changed
                if new_signal != last_signal:
                    st.write(f"Sentiment signal for {stock_ticker} changed to: **{new_signal}**")
                    send_imessage(recipient, f"The sentiment signal for {stock_ticker} has changed to {new_signal}.")
                    last_signal = new_signal
                else:
                    st.write(f"No change in sentiment signal for {stock_ticker}. Current signal: **{new_signal}**")

                # Update news content with dividers between articles and display articles
                for article in articles:
                    title = article.get('title', 'No title')
                    description = article.get('description', 'No description')
                    url = article.get('url', '#')
                    published_at = article.get('publishedAt', 'N/A')
                    news_content += f"**{title}**\n\n{description}\n\nPublished: {published_at}\n[Read more]({url})\n\n"
                    news_content += "---\n"  # Add a divider after each article

            else:
                news_content = f"No descriptions found in the articles for {stock_ticker} to analyze."
        else:
            news_content = f"No articles found for {stock_ticker}."

        # Display the updated news with dividers
        news_placeholder.markdown(f"### {stock_ticker} News\n" + news_content)

        # Wait for the specified interval before checking again
        time.sleep(check_interval)

# Function to monitor sentiment for multiple stocks
def monitor_multiple_stocks(stock_tickers, company_data, recipient, num_articles, check_interval=60):
    # Use a ThreadPoolExecutor to run sentiment monitoring for each stock in parallel
    with ThreadPoolExecutor() as executor:
        for stock_ticker in stock_tickers:
            executor.submit(monitor_single_stock, stock_ticker, company_data, recipient, num_articles, check_interval)

# Main function to show sentiment analysis and start monitoring
def show_sentiment_analysis():
    st.title("Live Stock Market News Sentiment Monitoring")

    # Load company data from CSV
    company_data = load_company_data()

    # Multi-select box to select stock tickers
    stock_tickers = st.multiselect("Select stock tickers to monitor:", options=list(company_data.keys()))

    # Input to select number of news articles to fetch
    num_articles = st.slider("Select the number of news articles to fetch for each stock:", min_value=1, max_value=20, value=10)

    # Input phone number for iMessage notifications
    recipient = st.text_input("Enter phone number to receive iMessage notifications (format: +1234567890):", value="+918287936541")

    # Interval to refresh and monitor news (in seconds)
    check_interval = st.slider("Set the time interval (seconds) between each sentiment check:", min_value=30, max_value=600, value=60)

    if st.button("Start Monitoring"):
        if stock_tickers:
            monitor_multiple_stocks(stock_tickers, company_data, recipient, num_articles, check_interval)
        else:
            st.error("Please select at least one stock ticker to monitor.")

# Run the Streamlit app
show_sentiment_analysis()

