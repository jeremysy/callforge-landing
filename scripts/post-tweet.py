#!/usr/bin/env python3
"""
Automated Twitter posting script for CallForgr
Reads tweets from twitter-posts.md and posts them on schedule
"""

import os
import json
import re
from pathlib import Path
import tweepy

# Configuration
TWEETS_FILE = Path(__file__).parent.parent / "twitter-posts.md"
STATE_FILE = Path(__file__).parent / "tweet-state.json"

def load_state():
    """Load the state of posted tweets"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted_indices": [], "last_post_date": None}

def save_state(state):
    """Save the state of posted tweets"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def parse_tweets():
    """Parse tweets from the markdown file"""
    with open(TWEETS_FILE, 'r') as f:
        content = f.read()

    # Split by post headers (### Post N:)
    posts = re.split(r'###\s+Post\s+\d+:', content)

    tweets = []
    for i, post in enumerate(posts[1:], 1):  # Skip first split (header content)
        # Get content between the title and the separator (---)
        lines = post.strip().split('\n')

        # Skip the title line, get content until ---
        tweet_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                break
            if line.strip():
                tweet_lines.append(line.strip())

        if tweet_lines:
            tweet_text = '\n'.join(tweet_lines)
            tweets.append({
                'index': i,
                'text': tweet_text
            })

    return tweets

def get_twitter_client():
    """Initialize Twitter API client"""
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not all([api_key, api_secret, access_token, access_secret]):
        raise ValueError("Twitter API credentials not found in environment variables")

    # Create client using OAuth 1.0a User Context
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    return client

def post_tweet(client, tweet_text):
    """Post a tweet using Twitter API v2"""
    try:
        response = client.create_tweet(text=tweet_text)
        return response.data['id']
    except Exception as e:
        print(f"Error posting tweet: {e}")
        raise

def main():
    """Main function to post next tweet"""
    print("Starting automated tweet posting...")

    # Load state
    state = load_state()
    posted_indices = set(state.get('posted_indices', []))

    # Parse tweets
    tweets = parse_tweets()
    print(f"Found {len(tweets)} tweets in total")
    print(f"Already posted: {len(posted_indices)} tweets")

    # Find next tweet to post
    next_tweet = None
    for tweet in tweets:
        if tweet['index'] not in posted_indices:
            next_tweet = tweet
            break

    if not next_tweet:
        print("All tweets have been posted! Restarting from beginning...")
        # Reset and start over
        posted_indices = set()
        next_tweet = tweets[0]

    # Get Twitter client
    client = get_twitter_client()

    # Post tweet
    print(f"\nPosting tweet #{next_tweet['index']}:")
    print(f"---\n{next_tweet['text']}\n---")

    tweet_id = post_tweet(client, next_tweet['text'])
    print(f"✅ Tweet posted successfully! ID: {tweet_id}")

    # Update state
    posted_indices.add(next_tweet['index'])
    state['posted_indices'] = sorted(list(posted_indices))
    state['last_post_date'] = os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
    state['last_tweet_id'] = tweet_id

    save_state(state)
    print(f"State updated. Posted {len(posted_indices)}/{len(tweets)} tweets")

if __name__ == "__main__":
    main()
