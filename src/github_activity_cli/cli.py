import argparse
import sys

from github_activity_cli.git_api import fetch_user_events
from github_activity_cli.events_format import format_events


def main():
    parser = argparse.ArgumentParser(
        prog="github-activity",
        description="Fetch and display recent public GitHub activity for a user"
    )

    parser.add_argument(
        "username",
        help="GitHub username to fetch activity for"
    )

    args = parser.parse_args()

    try:
        events = fetch_user_events(args.username)
        formatted_events = format_events(events)

        for line in formatted_events:
            print(line)

    except ValueError as error:
        print(f"{error}")
        sys.exit(1)

    except RuntimeError as error:
        print(f"{error}")
        sys.exit(1)


if __name__ == "__main__":
    main()

