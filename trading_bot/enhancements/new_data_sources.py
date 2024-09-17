import requests

def fetch_new_data():
    url = "https://api.example.com/market_data"
    response = requests.get(url)
    data = response.json()
    print("New data fetched.")
    return data

if __name__ == "__main__":
    data = fetch_new_data()
