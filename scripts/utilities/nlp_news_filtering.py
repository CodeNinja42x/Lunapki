import os
from dotenv import load_dotenv
import tweepy

# Load environment variables from .env file
load_dotenv()

# Get Twitter API credentials from environment variables
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET_KEY")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Set up Tweepy client for OAuth 2.0 Bearer Token usage (for reading tweets)
client_v2 = tweepy.Client(bearer_token=bearer_token)

# Set up Tweepy client for OAuth 1.0a (for posting tweets)
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
client_v1 = tweepy.API(auth)

def fetch_recent_tweets(query, max_results=10):
    """Fetch recent tweets based on a query using OAuth 2.0."""
    try:
        response = client_v2.search_recent_tweets(query=query, max_results=max_results)
        if response.data:
            return response.data
        else:
            print("No tweets found.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def post_tweet(content):
    """Post a tweet using OAuth 1.0a."""
    try:
        client_v1.update_status(status=content)
        print("Tweet posted successfully.")
    except Exception as e:
        print(f"An error occurred while posting the tweet: {e}")

if __name__ == "__main__":
    # Example usage: Fetch recent tweets containing the word "Python"
    tweets = fetch_recent_tweets(query="Python", max_results=5)
    if tweets:
        for tweet in tweets:
            print(f"Tweet: {tweet.text}")
    
    # Example: Post a sample tweet
    post_tweet("Hello, world! This is a test tweet from our automated bot.")
