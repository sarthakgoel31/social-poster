"""CLI entry point: python -m src"""
import argparse
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from .config import PROJECTS, list_projects
from .generator import generate_post
from .x_poster import post_thread, post_to_x


def _copy_to_clipboard(text: str) -> bool:
    """Copy text to macOS clipboard."""
    try:
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except Exception:
        return False


def main():
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    parser = argparse.ArgumentParser(
        prog="social-poster",
        description="Post your projects to Reddit (manual) and X/Twitter (automated)",
    )
    sub = parser.add_subparsers(dest="command")

    # --- list ---
    sub.add_parser("list", help="List all configured projects")

    # --- generate ---
    gen = sub.add_parser("generate", help="Generate post text")
    gen.add_argument("project", help="Project key from config")
    gen.add_argument("--platform", choices=["reddit", "x"], default="reddit")
    gen.add_argument("--subreddit", help="Target subreddit (for reddit)")
    gen.add_argument("--copy", action="store_true", help="Copy to clipboard")

    # --- reddit ---
    reddit = sub.add_parser("reddit", help="Generate Reddit post + copy to clipboard for manual posting")
    reddit.add_argument("project", help="Project key from config")
    reddit.add_argument("--subreddit", help="Target subreddit (posts to first configured if omitted)")

    # --- post (X only) ---
    post = sub.add_parser("post", help="Post to X/Twitter (automated)")
    post.add_argument("project", help="Project key from config")
    post.add_argument("--dry-run", action="store_true", help="Print tweet without sending")

    # --- post-thread (X only) ---
    thread = sub.add_parser("post-thread", help="Post a thread from a JSON file (array of tweet strings)")
    thread.add_argument("--json", required=True, help="Path to JSON array of tweets")
    thread.add_argument("--dry-run", action="store_true", help="Print thread without sending")

    args = parser.parse_args()

    if args.command == "list":
        list_projects()

    elif args.command == "generate":
        proj = PROJECTS.get(args.project)
        if not proj:
            print(f"Unknown project: {args.project}. Run 'list' to see available.")
            sys.exit(1)
        text = generate_post(proj, args.platform, args.subreddit)
        print(text)
        if args.copy and _copy_to_clipboard(text):
            print("\n--- Copied to clipboard! ---")

    elif args.command == "reddit":
        proj = PROJECTS.get(args.project)
        if not proj:
            print(f"Unknown project: {args.project}. Run 'list' to see available.")
            sys.exit(1)
        sr = args.subreddit or proj.get("subreddits", ["SideProject"])[0]
        text = generate_post(proj, "reddit", sr)

        # Split title and body for easy copy-paste
        parts = text.split("\n\n---\n\n", 1)
        title = parts[0].replace("TITLE: ", "").strip()
        body = parts[1].strip() if len(parts) > 1 else ""

        print(f"Subreddit: r/{sr}")
        print(f"Post URL:  https://www.reddit.com/r/{sr}/submit?type=self")
        print(f"\n{'='*60}")
        print(f"TITLE (copy this):")
        print(f"{'='*60}")
        print(title)
        print(f"\n{'='*60}")
        print(f"BODY (copy this):")
        print(f"{'='*60}")
        print(body)

        # Copy title to clipboard first (user pastes title, then runs again for body)
        if _copy_to_clipboard(title + "\n\n" + body):
            print(f"\n--- Full post copied to clipboard! ---")
            print(f"Open: https://www.reddit.com/r/{sr}/submit?type=self")

    elif args.command == "post":
        proj = PROJECTS.get(args.project)
        if not proj:
            print(f"Unknown project: {args.project}. Run 'list' to see available.")
            sys.exit(1)
        text = generate_post(proj, "x")
        if args.dry_run:
            print(f"[DRY RUN] X/Twitter ({len(text)} chars)")
            print(f"{'='*60}")
            print(text)
        else:
            post_to_x(text)

    elif args.command == "post-thread":
        import json

        tweets = json.loads(Path(args.json).read_text())
        if not isinstance(tweets, list) or not all(isinstance(t, str) for t in tweets):
            print("Expected a JSON array of tweet strings")
            sys.exit(1)
        if args.dry_run:
            print(f"[DRY RUN] Thread ({len(tweets)} tweets)")
            for i, t in enumerate(tweets, 1):
                print(f"{'='*60}\n{i}/ ({len(t)} chars)\n{t}")
        else:
            post_thread(tweets)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
