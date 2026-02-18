# Hacker News CLI

A simple, robust command-line tool to fetch and browse Hacker News stories using the public Firebase API. Supports listing top or new stories, viewing item details (title, URL, score, time), and threaded comments with graceful error handling and output limits.

## Installation

1. Clone the repository:
   ```
   git clone <repo-url>
   cd hackernews-cli
   ```

2. Install dependencies:
   ```
   pip install requests
   ```

3. Run the tool:
   ```
   python -m src.hackernews_cli top
   ```

## Usage

```
usage: hackernews_cli.py [-h] {top,new,show} ...

Hacker News CLI: Fetch top/new stories, show item details and comments.

positional arguments:
  {top,new,show}
    top           Show top stories
    new           Show new stories
    show          Show story details and comments

options:
  -h, --help      show this help message and exit

Examples:
  hackernews_cli.py top
  hackernews_cli.py top --limit 5
  hackernews_cli.py new --limit 10
  hackernews_cli.py show 38619777
```

Examples:

- Show top stories: `python -m src.hackernews_cli top`
- Show top 10 stories: `python -m src.hackernews_cli top --limit 10`
- Show new stories: `python -m src.hackernews_cli new --limit 10`
- Show story details and comments: `python -m src.hackernews_cli show 47064490`

## Features

- Fetch and list top or new stories with ID, score, truncated title, author, and comment count
- Display story details including title, URL, author, score, timestamp, and descendant count
- Render threaded comments recursively (max depth 6, first 20-30 kids per item)
- Pretty formatted console output
- Configurable `--limit` for story lists
- Robust error handling: skips failed fetches, handles deleted/missing items gracefully

## Dependencies

- Python 3.6+ (uses standard libraries: `argparse`, `sys`, `datetime`)
- `requests` (for API calls)

## Contributing

Fork the repo, make changes in `src/`, and submit a pull request. Tests can be added using the provided example args/stdout.

## License

MIT