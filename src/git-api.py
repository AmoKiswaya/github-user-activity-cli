import json
import time
import urllib.request
from urllib.error import HTTPError, URLError


def fetch_user_events(username):
    url = f"https://api.github.com/users/{username}/events"
    headers = {
        "Accept": "application/vnd.github+json"
    }

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
        
    except HTTPError as error:
        # 404 -> invalid username
        if error.code == 404:
            raise ValueError("User not found") from error 
        
        # 403 -> possibly rate-limited
        if error.code == 403:
            remaining = error.headers.get("X-RateLimit-Remaining")
            reset = error.headers.get("X-RateLimit-Reset")

            if remaining == "0" and reset:
                reset_time = time.strftime(
                    "%H:%M:%S",
                    time.localtime(int(reset))
                )
                raise RuntimeError(
                    f"Rate limit exceeded. Try again after {reset_time}"
                ) from error

            raise RuntimeError("Access forbidden by GitHub") from error

        raise RuntimeError(
            f"GitHub API error {error.code}: {error.reason}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Network error: {error.reason}"
        ) from error