# Social Poster

Automated posting agent for Reddit and X/Twitter. Generate platform-specific posts from your project configs and publish them with one command.

## Why

Friend got 3 paid projects from posting his 5 repos on Reddit/Twitter. I have 30+ projects. Same strategy, bigger pipeline.

## How

```
python -m src list                          # see all projects
python -m src generate archana --platform reddit  # preview a Reddit post
python -m src post archana --dry-run        # dry run to both platforms
python -m src post archana --platform reddit # go live on Reddit
python -m src post archana --platform both  # go live everywhere
```

## Features

| Feature | Detail |
|---|---|
| Platform-aware templates | Reddit gets long-form value posts, X gets punchy ≤280 char tweets |
| Subreddit tone matching | Technical subs get architecture talk, community subs get value framing |
| 9 projects configured | Archana, Second Brain, VidText, Call Analyzer, Trading Monitor, Morning Coffee, Kindle Agent, HisaabBot, Portfolio |
| Smart subreddit targeting | Each project maps to 3-4 relevant subreddits |
| Dry run mode | Preview everything before posting |
| Auth verification | `check_auth()` for both platforms |
| Claude Code skill | `/post` command for inline posting from terminal |

## Tech

| Component | Stack |
|---|---|
| Reddit API | PRAW (OAuth2 script app) |
| X/Twitter API | Tweepy v2 (OAuth 1.0a, free tier) |
| Post generation | Template engine with subreddit-specific tone |
| CLI | argparse with `list`, `generate`, `post` subcommands |
| Config | Python dict registry, no external deps |

## Architecture

```
social-poster/
├── src/
│   ├── __main__.py       # CLI entry point
│   ├── config.py         # Project registry + subreddit targeting
│   ├── generator.py      # Platform-specific post templates
│   ├── reddit_poster.py  # PRAW posting + auth check
│   └── x_poster.py       # Tweepy posting + auth check
├── .env                  # API credentials (not committed)
├── .env.example          # Credential template
└── requirements.txt      # praw, tweepy, python-dotenv
```

## Setup

```bash
cd personal/social-poster
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in API keys (see below)
```

### Reddit API Keys
1. Go to https://www.reddit.com/prefs/apps
2. Create app → **script** type
3. Copy client ID (under app name) and secret

### X/Twitter API Keys
1. Go to https://developer.x.com/en/portal/dashboard
2. Create project → Free tier
3. Generate API key, secret, access token, access token secret

## Status

| Item | Status |
|---|---|
| Post generator | Done |
| Reddit module | Done |
| X/Twitter module | Done |
| CLI | Done |
| `/post` skill | Done |
| Reddit account setup | Pending |
| X account setup | Pending |
| First post | Pending |
