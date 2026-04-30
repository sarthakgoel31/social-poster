# Social Poster

Post about your projects on Reddit and X/Twitter. Reddit = generate + copy-paste. X = automated via API.

## Why

Friend got 3 paid projects from posting his 5 repos on Reddit/Twitter. I have 30+ projects. Same strategy, bigger pipeline.

## How

```bash
python -m src list                                    # see all projects
python -m src reddit archana                          # generate Reddit post + copy to clipboard
python -m src reddit archana --subreddit hinduism     # target specific subreddit
python -m src post archana --dry-run                  # preview X tweet
python -m src post archana                            # post to X (automated)
python -m src generate archana --platform x --copy    # generate + copy to clipboard
```

## Features

| Feature | Detail |
|---|---|
| Reddit post generator | Long-form value posts, auto-copied to clipboard, opens submit URL |
| X/Twitter automation | Punchy ≤280 char tweets posted via API |
| Subreddit tone matching | Technical subs get architecture talk, community subs get value framing |
| 9 projects configured | Archana, Second Brain, VidText, Call Analyzer, Trading Monitor, Morning Coffee, Kindle Agent, HisaabBot, Portfolio |
| Smart subreddit targeting | Each project maps to 3-4 relevant subreddits |
| Clipboard integration | `pbcopy` on macOS — generated posts ready to paste |
| Claude Code skill | `/post` command for inline posting from terminal |

## Tech

| Component | Stack |
|---|---|
| X/Twitter API | Tweepy v2 (OAuth 1.0a, free tier) |
| Post generation | Template engine with subreddit-specific tone |
| CLI | argparse with `list`, `generate`, `reddit`, `post` subcommands |
| Clipboard | macOS `pbcopy` for instant copy |
| Config | Python dict registry, no external deps |

## Architecture

```
social-poster/
├── src/
│   ├── __main__.py       # CLI entry point
│   ├── config.py         # Project registry + subreddit targeting
│   ├── generator.py      # Platform-specific post templates
│   └── x_poster.py       # Tweepy posting + auth check
├── .env                  # X API credentials (not committed)
├── .env.example          # Credential template
└── requirements.txt      # tweepy, python-dotenv
```

## Setup

```bash
cd personal/social-poster
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in X/Twitter API keys
```

### X/Twitter API Keys
1. Go to https://developer.x.com/en/portal/dashboard
2. Create project → Free tier
3. Generate API key, secret, access token, access token secret

### Reddit (Manual)
No API needed. The `reddit` command generates the post, copies to clipboard, and gives you the submit URL.

## Status

| Item | Status |
|---|---|
| Post generator | Done |
| Reddit (manual + clipboard) | Done |
| X/Twitter module | Done |
| CLI | Done |
| `/post` skill | Done |
| X account setup | In progress |
| First post | Pending |
