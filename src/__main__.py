"""CLI entry point: python -m src"""
import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .config import PROJECTS, list_projects
from .generator import generate_post
from .reddit_poster import post_to_reddit
from .x_poster import post_to_x


def main():
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    parser = argparse.ArgumentParser(
        prog="social-poster",
        description="Post your projects to Reddit and X/Twitter",
    )
    sub = parser.add_subparsers(dest="command")

    # --- list ---
    sub.add_parser("list", help="List all configured projects")

    # --- generate ---
    gen = sub.add_parser("generate", help="Generate post text (dry run)")
    gen.add_argument("project", help="Project key from config")
    gen.add_argument("--platform", choices=["reddit", "x"], default="reddit")
    gen.add_argument("--subreddit", help="Target subreddit (for reddit)")

    # --- post ---
    post = sub.add_parser("post", help="Generate and post")
    post.add_argument("project", help="Project key from config")
    post.add_argument("--platform", choices=["reddit", "x", "both"], default="both")
    post.add_argument("--subreddit", help="Override target subreddit")
    post.add_argument("--dry-run", action="store_true", help="Print post without sending")

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
    elif args.command == "post":
        proj = PROJECTS.get(args.project)
        if not proj:
            print(f"Unknown project: {args.project}. Run 'list' to see available.")
            sys.exit(1)

        if args.platform in ("reddit", "both"):
            subreddits = [args.subreddit] if args.subreddit else proj.get("subreddits", [])
            for sr in subreddits:
                text = generate_post(proj, "reddit", sr)
                if args.dry_run:
                    print(f"\n{'='*60}")
                    print(f"[DRY RUN] r/{sr}")
                    print(f"{'='*60}")
                    print(text)
                else:
                    post_to_reddit(proj, sr, text)

        if args.platform in ("x", "both"):
            text = generate_post(proj, "x")
            if args.dry_run:
                print(f"\n{'='*60}")
                print(f"[DRY RUN] X/Twitter")
                print(f"{'='*60}")
                print(text)
            else:
                post_to_x(text)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
