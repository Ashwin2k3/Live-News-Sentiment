import streamlit as st
import requests
import csv
import time
from textblob import TextBlob
import pywhatkit as pwk  # Import pywhatkit for WhatsApp messaging

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

# Send WhatsApp notification when signal changes
def send_whatsapp_notification(ticker, new_signal, phone_number):
    message = f"The sentiment signal for {ticker} has changed to {new_signal}."
    
    try:
        # Get current time and add a 2-minute buffer to allow WhatsApp Web to load
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min + 2  # Sending the message 2 minutes ahead
        
        # Adjust hour and minute if it exceeds 60 minutes
        if minute >= 60:
            minute = minute % 60
            hour = (hour + 1) % 24  # Increment hour and wrap around if needed
        
        # Send WhatsApp message (phone number, message, hour, minute)
        pwk.sendwhatmsg(phone_number, message, hour, minute)
        st.success(f"WhatsApp notification scheduled for {hour:02d}:{minute:02d} to {phone_number}!")
    
    except Exception as e:
        st.error(f"Error sending WhatsApp message: {e}")
        
# Function to continuously monitor sentiment
def monitor_sentiment(stock_ticker, company_data, phone_number, check_interval=60):
    sentiment_pipeline = initialize_sentiment_pipeline()
    last_signal = None
    
    while True:
        with st.spinner("Fetching and analyzing news articles..."):
            query = company_data.get(stock_ticker, stock_ticker)
            articles = fetch_news(query, num_articles=10)

        if articles:
            texts = [article['description'] for article in articles if article['description']]
            if texts:
                sentiments = analyze_sentiments(sentiment_pipeline, texts)
                
                # Determine the new signal
                new_signal = get_signal_from_sentiments(sentiments)
                
                # Check if the signal has changed
                if new_signal != last_signal:
                    st.write(f"Sentiment signal changed to: **{new_signal}**")
                    send_whatsapp_notification(stock_ticker, new_signal, phone_number)
                    last_signal = new_signal
                else:
                    st.write(f"No change in sentiment signal. Current signal: **{new_signal}**")
            else:
                st.write("No descriptions found in the articles to analyze.")
        else:
            st.write("No articles found.")

        # Wait for the specified interval before checking again
        time.sleep(check_interval)

# Main function to show sentiment analysis and start monitoring
def show_sentiment_analysis():
    st.title("Live Stock Market News Sentiment Monitoring")

    # Load company data from CSV
    company_data = load_company_data()

    # Dropdown to select the stock ticker
    stock_ticker = st.selectbox("Select stock ticker to monitor:", options=list(company_data.keys()))

    # Input phone number for WhatsApp notifications
    phone_number = st.text_input("Enter phone number to receive WhatsApp notifications (format: +1234567890):", value="+918287936541")

    if st.button("Start Monitoring"):
        monitor_sentiment(stock_ticker, company_data, phone_number)

# Run the Streamlit app
show_sentiment_analysis()
