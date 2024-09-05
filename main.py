import streamlit as st
import requests
import csv
import time
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Send email notification when signal changes
def send_email_notification(ticker, new_signal):
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_email_password"
    
    subject = f"Sentiment Signal Change for {ticker}"
    body = f"The sentiment signal for {ticker} has changed to {new_signal}."
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        st.success(f"Email notification sent to {receiver_email}!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Function to continuously monitor sentiment
def monitor_sentiment(stock_ticker, company_data, check_interval=60):
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
                    st.write(f"Sentiment signal changed to: {new_signal}")
                    send_email_notification(stock_ticker, new_signal)
                    last_signal = new_signal
                else:
                    st.write(f"No change in sentiment signal. Current signal: {new_signal}")
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

    if st.button("Start Monitoring"):
        monitor_sentiment(stock_ticker, company_data)

# Run the Streamlit app
show_sentiment_analysis()

