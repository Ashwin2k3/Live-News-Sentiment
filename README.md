# Live-News-Sentiment

## live news sentiment for multiple stocks and notification via imessages
### Documentation for Stock Market Sentiment Monitoring App

This Python-based Streamlit application provides real-time monitoring of stock market news sentiment. It fetches live news articles related to selected stocks, analyzes their sentiment, and sends iMessage notifications if the sentiment changes.

---

### Libraries Used
1. **Streamlit (`st`)**: For building and displaying the web interface.
2. **Requests (`requests`)**: For making HTTP requests to the News API.
3. **CSV (`csv`)**: For reading stock symbol and name data from a CSV file.
4. **Time (`time`)**: For managing the intervals between checks.
5. **TextBlob (`TextBlob`)**: For sentiment analysis of the news articles.
6. **Subprocess (`subprocess`)**: To send iMessage notifications via AppleScript.
7. **ThreadPoolExecutor**: For monitoring multiple stocks concurrently.

---

### Application Workflow

1. **Load Company Data**: 
   - Reads company stock symbols and names from a CSV file (`stock.csv`).
   - The CSV file should contain `Symbol` and `Name` columns.

   ```python
   def load_company_data(file_path='stock.csv'):
       ...
   ```

2. **Fetch News from News API**:
   - Makes an API call to News API to retrieve articles based on a query (stock name or symbol).
   - The query returns up to `num_articles` news articles.

   ```python
   def fetch_news(query, num_articles=10, language='en'):
       ...
   ```

3. **Sentiment Analysis**:
   - Initializes a pipeline using `TextBlob` for analyzing the polarity of news descriptions.
   - Positive polarity (> 0) suggests positive sentiment, negative polarity (< 0) suggests negative sentiment.

   ```python
   def analyze_sentiments(sentiment_pipeline, texts):
       ...
   ```

4. **Market Signal Based on Sentiment**:
   - Generates a "Buy," "Sell," or "Hold" signal based on the proportion of positive and negative sentiments in the articles.

   ```python
   def get_signal_from_sentiments(sentiments):
       ...
   ```

5. **Send iMessage Notifications**:
   - Sends an iMessage using AppleScript when there is a change in market sentiment or new information is available.
   - This function will format the message, including details like title, sentiment, and the link to the article.

   ```python
   def send_imessage(recipient, stock_ticker, news_title, news_description, news_sentiment, market_sentiment, imessage_content, news_url):
       ...
   ```

6. **Monitor Single Stock**:
   - Continuously fetches news articles, performs sentiment analysis, and compares the results to the last checked signal.
   - Sends notifications if there is a change in sentiment signal.

   ```python
   def monitor_single_stock(stock_ticker, company_data, recipient, num_articles, check_interval=60):
       ...
   ```

7. **Monitor Multiple Stocks**:
   - Allows monitoring of multiple stocks simultaneously by using a thread pool. Each stock is processed by a separate thread that monitors news and sends notifications independently.

   ```python
   def monitor_multiple_stocks(stock_tickers, company_data, recipient, num_articles, check_interval=60):
       ...
   ```

8. **Main Interface**:
   - The user selects the stocks to monitor, the number of news articles to fetch, the time interval between checks, and the recipient for iMessage notifications.
   - Starts the monitoring process when the user clicks "Start Monitoring."

   ```python
   def show_sentiment_analysis():
       ...
   ```

---

### Key Features

- **Real-Time News Fetching**: Retrieves the latest news articles related to the selected stocks from the News API.
- **Sentiment Analysis**: Uses `TextBlob` to perform sentiment analysis on the fetched news descriptions, determining positive, negative, or neutral sentiment.
- **Market Sentiment Signals**: Generates "Buy," "Sell," or "Hold" signals based on the overall sentiment of the articles.
- **iMessage Notifications**: Sends notifications via iMessage when a stock's sentiment signal changes.
- **Concurrency**: Monitors multiple stocks in parallel using threads, ensuring performance efficiency.

---

### Configuration

- **News API Key**: The API key for News API must be set in the `fetch_news` function (`api_key` variable).
- **iMessage Notification**: The application uses AppleScript to send iMessages. This functionality is specific to macOS systems.
  
---

### How to Use

1. Ensure you have the following dependencies installed:
   ```bash
   pip install streamlit requests textblob
   ```
   
2. Place the CSV file (`stock.csv`) in the same directory as your script. The file should contain stock symbols and names in the following format:

   | Symbol | Name         |
   |--------|--------------|
   | AAPL   | Apple Inc.    |
   | TSLA   | Tesla Motors  |
   
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Select stock tickers, set the number of articles, and start monitoring.
