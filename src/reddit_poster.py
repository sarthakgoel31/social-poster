"""Post to Reddit via PRAW (Python Reddit API Wrapper)."""

import os
import praw


def _get_client() -> praw.Reddit:
    """Create authenticated Reddit client."""
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    username = os.environ.get("REDDIT_USERNAME")
    password = os.environ.get("REDDIT_PASSWORD")
    user_agent = os.environ.get("REDDIT_USER_AGENT", "social-poster/1.0")

    if not all([client_id, client_secret, username, password]):
        raise RuntimeError(
            "Missing Reddit credentials. Set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, "
            "REDDIT_USERNAME, REDDIT_PASSWORD in .env"
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
    )


def post_to_reddit(proj: dict, subreddit: str, generated_text: str):
    """Post to a subreddit. generated_text has TITLE: ... then body after ---."""
    parts = generated_text.split("\n\n---\n\n", 1)
    title = parts[0].replace("TITLE: ", "").strip()
    body = parts[1].strip() if len(parts) > 1 else ""

    reddit = _get_client()
    sub = reddit.subreddit(subreddit)

    submission = sub.submit(title=title, selftext=body)
    print(f"Posted to r/{subreddit}: {submission.url}")
    return submission


def check_auth():
    """Verify Reddit credentials work."""
    try:
        reddit = _get_client()
        user = reddit.user.me()
        print(f"Authenticated as: u/{user.name}")
        print(f"Karma: {user.link_karma} link / {user.comment_karma} comment")
        return True
    except Exception as e:
        print(f"Reddit auth failed: {e}")
        return False
