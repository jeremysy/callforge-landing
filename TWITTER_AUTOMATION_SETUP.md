# Twitter Automation Setup Guide

This guide will help you set up automated tweet posting for CallForgr using GitHub Actions.

## Overview

The automation system:
- Posts tweets from `twitter-posts.md` automatically
- Runs on schedule: **Monday, Wednesday, Friday at 10:00 AM ET**
- Tracks which tweets have been posted (in `scripts/tweet-state.json`)
- Cycles through all tweets, then starts over
- Can be triggered manually from GitHub Actions tab

## Setup Instructions

### Step 1: Get Twitter API Credentials

1. **Apply for Twitter Developer Account**
   - Go to https://developer.twitter.com/
   - Click "Sign up" or "Apply"
   - Fill out the application (select "Hobbyist" → "Making a bot")
   - Wait for approval (usually instant to 24 hours)

2. **Create a Twitter App**
   - Go to https://developer.twitter.com/en/portal/dashboard
   - Click "Create App" or "Create Project"
   - Name your app (e.g., "CallForgr Auto Poster")
   - Save your API Key and API Secret Key

3. **Generate Access Tokens**
   - In your app settings, go to "Keys and tokens"
   - Under "Authentication Tokens", click "Generate" for Access Token and Secret
   - Save these tokens immediately (you can't see them again!)

4. **Set App Permissions**
   - Go to app "Settings" → "User authentication settings"
   - Enable "OAuth 1.0a"
   - Set permissions to "Read and write"
   - Save changes

5. **Get Bearer Token** (if not shown)
   - In "Keys and tokens" tab
   - Under "Bearer Token", click "Generate"
   - Save this token

You should now have:
- ✅ API Key (Consumer Key)
- ✅ API Secret Key (Consumer Secret)
- ✅ Access Token
- ✅ Access Token Secret
- ✅ Bearer Token

### Step 2: Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret" and add each of these:

   | Secret Name | Value |
   |-------------|-------|
   | `TWITTER_API_KEY` | Your API Key (Consumer Key) |
   | `TWITTER_API_SECRET` | Your API Secret Key (Consumer Secret) |
   | `TWITTER_ACCESS_TOKEN` | Your Access Token |
   | `TWITTER_ACCESS_SECRET` | Your Access Token Secret |
   | `TWITTER_BEARER_TOKEN` | Your Bearer Token |

4. Click "Add secret" for each one

### Step 3: Enable GitHub Actions

1. Go to your repository's "Actions" tab
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. You should see the "Auto Post Tweets" workflow

### Step 4: Test the Setup

**Manual Test:**
1. Go to "Actions" tab
2. Click "Auto Post Tweets" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait ~30 seconds and check if the tweet was posted to @callforge
5. Check the workflow logs for any errors

**Scheduled Posts:**
- The workflow will automatically run Mon/Wed/Fri at 10:00 AM ET (14:00 UTC)
- You can modify the schedule in `.github/workflows/post-tweets.yml`

## How It Works

### Tweet Selection
- Reads all tweets from `twitter-posts.md`
- Posts them in order (Post 1, Post 2, Post 3, etc.)
- Skips threads (marked as "Thread N:") - you post these manually
- When all tweets are posted, it loops back to the beginning

### State Tracking
- `scripts/tweet-state.json` tracks which tweets have been posted
- This file is automatically committed back to the repo after each post
- You can manually reset it to repost tweets

### Customizing the Schedule

Edit `.github/workflows/post-tweets.yml`:

```yaml
schedule:
  # Current: Mon/Wed/Fri at 10 AM ET
  - cron: '0 14 * * 1,3,5'

  # Daily at 10 AM ET:
  - cron: '0 14 * * *'

  # Twice daily (10 AM and 2 PM ET):
  - cron: '0 14,18 * * *'

  # Every weekday at 10 AM ET:
  - cron: '0 14 * * 1-5'
```

Cron format: `minute hour day month weekday` (times in UTC)
- ET to UTC: Add 5 hours (or 4 during DST)

## Managing Tweets

### Adding New Tweets
1. Edit `twitter-posts.md`
2. Add new posts following the format:
   ```markdown
   ### Post N: Title
   Tweet text here...

   #Hashtags #GoHere

   ---
   ```
3. Commit and push
4. The new tweets will be picked up automatically

### Resetting the Queue
To repost all tweets from the beginning:
1. Edit `scripts/tweet-state.json`
2. Change to:
   ```json
   {
     "posted_indices": [],
     "last_post_date": null
   }
   ```
3. Commit and push

### Pausing Automation
To temporarily pause:
1. Go to "Actions" → "Auto Post Tweets"
2. Click "⋯" → "Disable workflow"

To resume:
- Click "Enable workflow"

## Troubleshooting

### "Twitter API credentials not found"
- Check that all 5 secrets are added in GitHub Settings → Secrets
- Secret names must match exactly (case-sensitive)

### "Error posting tweet: 403 Forbidden"
- Check app permissions are set to "Read and write"
- Regenerate Access Token after changing permissions

### "Duplicate tweet"
- Twitter blocks posting the same text twice
- Add variation to your tweets or wait before reposting

### Tweet posted but state not updated
- Check GitHub Actions has write permissions
- Go to Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

### Schedule not working
- GitHub Actions can have delays of 3-10 minutes
- Check the "Actions" tab for workflow runs
- Verify cron schedule is in UTC time

## Manual Posting

You can also run the script locally:

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Set environment variables
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_SECRET="your_token_secret"
export TWITTER_BEARER_TOKEN="your_bearer"

# Run script
python scripts/post-tweet.py
```

## Security Notes

- ✅ Never commit API keys to the repository
- ✅ Only store them in GitHub Secrets
- ✅ Regenerate tokens if accidentally exposed
- ✅ Review Twitter's automation rules: https://help.twitter.com/en/rules-and-policies/twitter-automation

## Support

If you encounter issues:
1. Check the GitHub Actions logs for detailed error messages
2. Verify all credentials are correct
3. Test with manual workflow trigger first
4. Check Twitter's API status: https://api.twitterstatus.com/

---

Ready to automate! Once set up, your CallForgr tweets will post automatically 3x per week. 🚀
