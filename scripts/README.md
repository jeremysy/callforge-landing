# Twitter Automation Scripts

This directory contains the automated Twitter posting system for CallForgr.

## Files

- **`post-tweet.py`** - Main script that posts tweets using Twitter API v2
- **`requirements.txt`** - Python dependencies (tweepy)
- **`tweet-state.json`** - Tracks which tweets have been posted (auto-updated)

## How to Use

### Automated (Recommended)
The GitHub Action (`.github/workflows/post-tweets.yml`) runs this automatically on schedule.

See `TWITTER_AUTOMATION_SETUP.md` in the root directory for setup instructions.

### Manual Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables with your Twitter API credentials
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
export TWITTER_BEARER_TOKEN="your_bearer_token"

# Run the script
python post-tweet.py
```

## What It Does

1. Reads tweets from `../twitter-posts.md`
2. Checks `tweet-state.json` to see which tweets have been posted
3. Posts the next unposted tweet
4. Updates `tweet-state.json` with the new state
5. Loops back to the beginning when all tweets are posted

## Modifying Tweets

Edit `../twitter-posts.md` and add tweets in this format:

```markdown
### Post N: Title
Your tweet text here...

Can be multiple lines.

#Hashtags

---
```

The script will automatically detect and post new tweets.
