"""Generate platform-specific posts from project config.

Templates are designed to feel authentic on each platform:
- Reddit: longer, value-first, no hard sell, show the work
- X: punchy, thread-friendly, hashtags, link at end
"""

from typing import Optional

# Subreddit-specific tone adjustments
SUBREDDIT_TONES = {
    # Dev communities — lead with tech, show architecture
    "Python": "technical",
    "webdev": "technical",
    "nextjs": "technical",
    "reactjs": "technical",
    "MachineLearning": "technical",
    "artificial": "technical",
    "algotrading": "technical",
    # Side project communities — lead with problem/solution
    "SideProject": "builder",
    "startups": "builder",
    "SaaS": "builder",
    # Interest communities — lead with value to THEM
    "hinduism": "community",
    "india": "community",
    "kindle": "community",
    "personalfinance": "community",
    "productivity": "community",
    "Daytrading": "community",
    "FuturesTrading": "community",
}


def _reddit_title(proj: dict, subreddit: str) -> str:
    """Generate a Reddit post title."""
    tone = SUBREDDIT_TONES.get(subreddit, "builder")
    name = proj["name"]
    tagline = proj["tagline"]

    if tone == "technical":
        return f"I built {name} — {tagline} [Open Source]"
    elif tone == "community":
        return f"{name}: {tagline}"
    else:  # builder
        return f"I built {name} — {tagline}"


def _reddit_body(proj: dict, subreddit: str) -> str:
    """Generate a Reddit post body."""
    tone = SUBREDDIT_TONES.get(subreddit, "builder")
    highlights = proj.get("highlights", [])
    repo = proj.get("repo", "")
    url = proj.get("url")

    lines = []

    # Opening — varies by tone
    if tone == "technical":
        lines.append(f"Been working on **{proj['name']}** and wanted to share the technical approach.\n")
    elif tone == "community":
        lines.append(f"Built something that might be useful for this community.\n")
    else:
        lines.append(f"Hey! I've been building **{proj['name']}** as a side project and just open-sourced it.\n")

    # What it does
    lines.append(f"## What it does\n")
    lines.append(f"{proj['tagline']}.\n")

    # Key features
    if highlights:
        lines.append(f"## Highlights\n")
        for h in highlights:
            lines.append(f"- {h}")
        lines.append("")

    # Links
    lines.append("## Links\n")
    if url:
        lines.append(f"- **Live:** {url}")
    lines.append(f"- **GitHub:** https://github.com/{repo}")
    lines.append("")

    # Closing — invite feedback
    if tone == "technical":
        lines.append("Would love feedback on the architecture. Happy to answer questions about the implementation.")
    elif tone == "community":
        lines.append("Free to use. Would love to hear if this is useful for you.")
    else:
        lines.append("Completely free and open source. Feedback welcome!")

    return "\n".join(lines)


def _x_post(proj: dict) -> str:
    """Generate an X/Twitter post (≤280 chars for main tweet)."""
    name = proj["name"]
    tagline = proj["tagline"]
    repo = proj.get("repo", "")
    url = proj.get("url")
    hashtags = " ".join(proj.get("x_hashtags", [])[:3])

    link = url or f"https://github.com/{repo}"

    # Build tweet — keep under 280 chars
    tweet = f"I built {name} — {tagline}\n\n"

    # Add top 3 highlights as bullet points
    highlights = proj.get("highlights", [])[:3]
    for h in highlights:
        bullet = f"- {h}\n"
        if len(tweet) + len(bullet) + len(link) + len(hashtags) + 5 < 280:
            tweet += bullet

    tweet += f"\n{link}\n\n{hashtags}"

    # If too long, trim to just tagline + link + hashtags
    if len(tweet) > 280:
        tweet = f"I built {name} — {tagline}\n\n{link}\n\n{hashtags}"

    # Final trim if still over
    if len(tweet) > 280:
        tweet = f"{name}: {tagline}\n\n{link}"

    return tweet.strip()


def generate_post(proj: dict, platform: str, subreddit: Optional[str] = None) -> str:
    """Generate a post for the given platform.

    Returns the full post text. For Reddit, returns title + body separated by a line.
    """
    if platform == "reddit":
        sr = subreddit or (proj.get("subreddits", ["SideProject"])[0])
        title = _reddit_title(proj, sr)
        body = _reddit_body(proj, sr)
        return f"TITLE: {title}\n\n---\n\n{body}"
    elif platform == "x":
        return _x_post(proj)
    else:
        raise ValueError(f"Unknown platform: {platform}")
