"""Post to X/Twitter via tweepy (OAuth 1.0a for posting)."""

import os
import tweepy


def _get_client() -> tweepy.Client:
    """Create authenticated X/Twitter client (v2 API)."""
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        raise RuntimeError(
            "Missing X/Twitter credentials. Set X_API_KEY, X_API_SECRET, "
            "X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET in .env"
        )

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )


def post_to_x(text: str):
    """Post a tweet. Text should be ≤280 chars."""
    if len(text) > 280:
        print(f"Warning: Tweet is {len(text)} chars (max 280). Truncating...")
        text = text[:277] + "..."

    client = _get_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Posted to X: https://x.com/i/status/{tweet_id}")
    return response


def check_auth():
    """Verify X/Twitter credentials work."""
    try:
        client = _get_client()
        user = client.get_me()
        print(f"Authenticated as: @{user.data.username}")
        return True
    except Exception as e:
        print(f"X auth failed: {e}")
        return False


def post_thread(tweets: list[str]) -> str:
    """Post a thread — each tweet replies to the previous. Returns the first tweet's URL."""
    if not tweets:
        raise ValueError("Empty thread")
    client = _get_client()
    first_id = None
    prev_id = None
    for text in tweets:
        if len(text) > 280:
            print(f"Warning: tweet is {len(text)} chars (max 280). Truncating...")
            text = text[:277] + "..."
        response = client.create_tweet(text=text, in_reply_to_tweet_id=prev_id)
        prev_id = response.data["id"]
        if first_id is None:
            first_id = prev_id
    url = f"https://x.com/i/status/{first_id}"
    print(f"Posted thread ({len(tweets)} tweets): {url}")
    return url
