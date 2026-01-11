#!/usr/bin/env python3
"""
Delete a specific tweet by ID
"""
import os
import sys
import tweepy

def get_twitter_client():
    """Create and return authenticated Twitter API client"""
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_secret = os.environ.get('TWITTER_ACCESS_SECRET')
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

    if not all([api_key, api_secret, access_token, access_secret, bearer_token]):
        raise ValueError("Twitter API credentials not found in environment variables")

    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    return client

def delete_tweet(tweet_id):
    """Delete a specific tweet"""
    try:
        client = get_twitter_client()
        client.delete_tweet(tweet_id)
        print(f"✓ Tweet {tweet_id} deleted successfully!")
        return True
    except Exception as e:
        print(f"✗ Error deleting tweet: {str(e)}")
        return False

if __name__ == "__main__":
    # Delete the specific tweet with wrong URL
    tweet_id = "2010139870748881009"

    print(f"Deleting tweet ID: {tweet_id}")
    success = delete_tweet(tweet_id)
    sys.exit(0 if success else 1)
