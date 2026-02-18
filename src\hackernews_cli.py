import argparse
import requests
import sys
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0/"

def fetch_stories(story_type, limit):
    if limit <= 0:
        return []
    try:
        resp = requests.get(f"{BASE_URL}{story_type}stories.json", timeout=10)
        resp.raise_for_status()
        ids = resp.json()
    except (requests.RequestException, ValueError):
        return []
    if not ids:
        return []
    ids = ids[:limit]
    stories = []
    for iid in ids:
        try:
            resp = requests.get(f"{BASE_URL}item/{iid}.json", timeout=10)
            resp.raise_for_status()
            item = resp.json()
            if item and item.get('type') == 'story':
                stories.append(item)
        except (requests.RequestException, ValueError):
            pass
    return stories

def print_story_list(stories, story_type):
    print(f"\n{story_type.upper()} Stories:\n")
    for i, story in enumerate(stories, 1):
        id_ = story.get('id', 0)
        title = story.get('title', 'N/A')
        if len(title) > 70:
            title = title[:70] + '...'
        score = story.get('score', 0)
        by_ = story.get('by', 'unknown')
        desc = story.get('descendants', 0)
        print(f"{i:2d}. {id_:>8d} ({score:>3} pts) {title}")
        print(f"     by {by_} | {desc:>3} comments")
    print()

def print_item(item, depth=0, max_depth=6):
    if depth > max_depth or not item or 'type' not in item:
        return
    indent = "  " * depth
    itype = item['type']
    if itype == 'story':
        title = item.get('title', 'N/A')
        print(f"{indent}Title: {title}")
        url = item.get('url')
        if url:
            print(f"{indent}URL: {url}")
        print(f"{indent}Author: {item.get('by', 'N/A')}")
        print(f"{indent}Score: {item.get('score', 0)}")
        if 'time' in item:
            time_str = datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M')
        else:
            time_str = 'N/A'
        print(f"{indent}Time: {time_str}")
        print(f"{indent}Comments: {item.get('descendants', 0)}")
    elif itype == 'comment':
        print(f"{indent}{item.get('by', 'N/A')}:")
        text = item.get('text', '')
        text_lines = text.split('\n')
        for line in text_lines:
            print(f"{indent}  {line}")
    print()

def print_comments(cid, depth=0, max_depth=6):
    if depth > max_depth:
        return
    try:
        resp = requests.get(f"{BASE_URL}item/{cid}.json", timeout=10)
        resp.raise_for_status()
        comment = resp.json()
        if comment:
            print_item(comment, depth, max_depth)
            kids = comment.get('kids')
            if kids and depth < max_depth:
                for kid_id in kids[:20]:
                    print_comments(kid_id, depth + 1, max_depth)
    except (requests.RequestException, ValueError):
        pass

def show_item(item_id):
    try:
        resp = requests.get(f"{BASE_URL}item/{item_id}.json", timeout=10)
        resp.raise_for_status()
        item = resp.json()
        if not item:
            print(f"Item {item_id} not found or deleted.", file=sys.stderr)
            sys.exit(1)
        print_item(item, 0)
        if item.get('kids'):
            print("\n--- Comments ---\n")
            for kid_id in item['kids'][:30]:
                print_comments(kid_id, 1)
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching item {item_id}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Hacker News CLI: Fetch top/new stories, show item details and comments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s top
  %(prog)s top --limit 5
  %(prog)s new --limit 10
  %(prog)s show 38619777
        """
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    top_parser = subparsers.add_parser('top', help='Show top stories')
    top_parser.add_argument('--limit', '-l', type=int, default=10, help='Number of stories (default: 10)')

    new_parser = subparsers.add_parser('new', help='Show new stories')
    new_parser.add_argument('--limit', '-l', type=int, default=10, help='Number of stories (default: 10)')

    show_parser = subparsers.add_parser('show', help='Show story details and comments')
    show_parser.add_argument('id', type=int, help='Hacker News item ID')

    args = parser.parse_args()

    if args.command == 'top':
        if args.limit < 1:
            print("Limit must be positive.", file=sys.stderr)
            sys.exit(1)
        stories = fetch_stories('top', args.limit)
        print_story_list(stories, 'Top')
    elif args.command == 'new':
        if args.limit < 1:
            print("Limit must be positive.", file=sys.stderr)
            sys.exit(1)
        stories = fetch_stories('new', args.limit)
        print_story_list(stories, 'New')
    elif args.command == 'show':
        show_item(args.id)

if __name__ == "__main__":
    main()
