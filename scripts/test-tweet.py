#!/usr/bin/env python3
"""
Quick diagnostic script to test Twitter API connection (read-only)
"""

import os
import tweepy

api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret = os.getenv('TWITTER_ACCESS_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

print("Testing Twitter API credentials...")

try:
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    print("✅ Client created successfully")

    me = client.get_me()
    print(f"✅ Authenticated as: @{me.data.username}")

except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 50)
