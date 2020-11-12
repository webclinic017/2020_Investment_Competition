import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/aapl/prices?startDate=2015-01-02&columns=adjClose&token=949f9442cbdff3e5ad488d93280c0b92ef042449", headers=headers)
print(requestResponse.json())