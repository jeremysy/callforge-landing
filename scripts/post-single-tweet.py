#!/usr/bin/env python3
"""
Post a single tweet immediately (for announcements, blog posts, etc.)
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

def post_tweet(tweet_text):
    """Post a single tweet"""
    try:
        client = get_twitter_client()
        response = client.create_tweet(text=tweet_text)
        print(f"✓ Tweet posted successfully!")
        print(f"Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"✗ Error posting tweet: {str(e)}")
        return False

if __name__ == "__main__":
    # Tweet about the new blog post
    tweet = """Anthropic's CEO talks about "living in a parallel universe" when working in AI.

Your business might be in one too - where copy-paste is still how work gets done.

New post on what this means for automation:
https://callforge.com/blog/parallel-universe-automation.html

#Automation #AI"""

    print("Posting tweet about new blog post...")
    print(f"\nTweet text:\n{tweet}\n")

    success = post_tweet(tweet)
    sys.exit(0 if success else 1)
