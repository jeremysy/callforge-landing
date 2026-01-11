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

def get_recent_tweets():
    """Get recent tweets from the authenticated user"""
    try:
        client = get_twitter_client()
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id

        # Get recent tweets
        tweets = client.get_users_tweets(user_id, max_results=10)

        if tweets.data:
            print(f"\nFound {len(tweets.data)} recent tweets:\n")
            for i, tweet in enumerate(tweets.data, 1):
                print(f"{i}. ID: {tweet.id}")
                print(f"   Text: {tweet.text[:100]}...")
                print()
            return tweets.data
        else:
            print("No tweets found")
            return []
    except Exception as e:
        print(f"Error getting tweets: {str(e)}")
        return []

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
    print("Fetching recent tweets to find the one with wrong URL...")
    tweets = get_recent_tweets()

    # Look for tweet with "callforge.com" (wrong URL)
    tweet_to_delete = None
    for tweet in tweets:
        if "callforge.com/blog/parallel" in tweet.text:
            tweet_to_delete = tweet
            break

    if tweet_to_delete:
        print(f"\n🎯 Found tweet with wrong URL:")
        print(f"ID: {tweet_to_delete.id}")
        print(f"Text: {tweet_to_delete.text}\n")
        print("Deleting...")
        success = delete_tweet(tweet_to_delete.id)
        sys.exit(0 if success else 1)
    else:
        print("\nNo tweet found with 'callforge.com' - it may have already been deleted.")
        sys.exit(0)
