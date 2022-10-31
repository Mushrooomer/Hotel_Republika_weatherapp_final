# This app is meant to run every morning at 9:00 on PythonAnywhere to czech if it's sunny in front of Hotel Republika.
# It supposed to notify the receptionist to open the front windows.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = "1a9f1cb019166ecb22e75b75e9aaca7b"
account_sid = "AC22c3a35e1d483648dede0498ddf949f6"
auth_token = "888fbaa4cb5cb511c7df6467460eeec5"


weather_params = {
    "lat": 50.091322,
    "lon": 14.433097,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

its_sunny_open_window = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) == 800:
        its_sunny_open_window = True

if its_sunny_open_window:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Otevrit okna, je jasno! :D",
        from_='+420460003500',
        to="+420778431699"
    )
    print(message.status)
