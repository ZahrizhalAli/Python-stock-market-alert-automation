import requests
import datetime as dt
from decouple import config
from twilio.rest import Client

account_sid = config('ACCOUNT_SID')
auth_token = config('AUTH_TOKEN')
client = Client(account_sid, auth_token)

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
# print(yesterday_closing_data)

before_yesterday = data_list[1]
before_yesterday_closing_data = before_yesterday['4. close']
# print(before_yesterday_closing_data)

difference_price = abs(float(yesterday_closing_data) - float(before_yesterday_closing_data))
# print(difference_price)
up_down = None
if difference_price > 0:
    up_down = "⬆"
else:
    up_down = "⬇"


diff_percent = (difference_price / float(yesterday_closing_data)) * 100
# print(f"{diff_percent}%")

if diff_percent >= 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    # print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{round(diff_percent)}% \nHeadline: {article['title']}. "
                          f"\n Brief: {article['description']}" for article in three_articles]
    for ar in formatted_articles:
        message = client.messages \
            .create(
            body=ar,
            from_='YOUR_PHONE_NUMBER_API_SERVICE',
            to='YOUR_PHONE_NUMBER'
        )




