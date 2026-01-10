#!/usr/bin/env python3
"""
Quick diagnostic script to test Twitter API connection
"""

import os
import tweepy

# Get credentials
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret = os.getenv('TWITTER_ACCESS_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

print("Testing Twitter API credentials...")
print(f"API Key: {api_key[:10]}..." if api_key else "❌ Missing")
print(f"API Secret: {api_secret[:10]}..." if api_secret else "❌ Missing")
print(f"Access Token: {access_token[:10]}..." if access_token else "❌ Missing")
print(f"Access Secret: {access_secret[:10]}..." if access_secret else "❌ Missing")
print(f"Bearer Token: {bearer_token[:10]}..." if bearer_token else "❌ Missing")

try:
    # Create client
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    print("\n✅ Client created successfully")

    # Try to get user info (read-only test)
    print("\nTesting read access...")
    me = client.get_me()
    print(f"✅ Authenticated as: @{me.data.username}")

    # Try to post a test tweet
    print("\nTesting write access...")
    test_text = "Testing automated posting from CallForgr! 🚀 #TestTweet"
    print(f"Attempting to post: {test_text}")

    response = client.create_tweet(text=test_text)
    print(f"✅ Tweet posted successfully!")
    print(f"Tweet ID: {response.data['id']}")
    print(f"View at: https://twitter.com/i/web/status/{response.data['id']}")

except tweepy.errors.Forbidden as e:
    print(f"\n❌ Permission Error: {e}")
    print("\nThis usually means:")
    print("1. Your app doesn't have write permissions")
    print("2. Go to https://developer.twitter.com/en/portal/dashboard")
    print("3. Select your app → Settings → User authentication settings")
    print("4. Make sure 'Read and write' permissions are enabled")
    print("5. Regenerate your Access Token and Secret after changing permissions")

except tweepy.errors.Unauthorized as e:
    print(f"\n❌ Authentication Error: {e}")
    print("\nYour credentials are invalid or expired.")
    print("Double-check all 5 secrets in GitHub")

except Exception as e:
    print(f"\n❌ Unexpected error: {type(e).__name__}")
    print(f"Message: {e}")

print("\n" + "="*50)
