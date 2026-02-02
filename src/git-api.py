import json
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
        if error.code == 404:
            raise ValueError("User not found") from error 
        raise RuntimeError(
            f"GitHub API error {error.code}: {error.reason}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Network error: {error.reason}"
        ) from error