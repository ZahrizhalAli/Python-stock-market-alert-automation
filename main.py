import requests
import datetime as dt
from decouple import config

time = dt.datetime.now(dt.timezone.utc)
time_now = str(time)
today = time_now.split(" ")[0]
print("Today is " + today)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = config("ALPHA_API_KEY")
NEWS_API_KEY = config("NEWS_API_KEY")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}

news_params = {
    'apiKey' : NEWS_API_KEY,
    'qInTitle': COMPANY_NAME
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]  # List Comprehension
yesterday_data = data_list[0]
yesterday_closing_data = yesterday_data['4. close']
print(yesterday_closing_data)

before_yesterday = data_list[1]
before_yesterday_closing_data = before_yesterday['4. close']
print(before_yesterday_closing_data)

difference_price = abs(float(yesterday_closing_data) - float(before_yesterday_closing_data))
print(difference_price)

diff_percent = (difference_price / float(yesterday_closing_data)) * 100
print(f"{diff_percent}%")

if diff_percent > 0:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    print(three_articles)
#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

