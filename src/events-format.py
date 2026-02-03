def handle_watch_event(event):
    user = event["actor"]["login"]
    repo = event["repo"]["name"]
    return f"{user} starred {repo}" 

def handle_push_event(event):
    user = event["actor"]["login"]
    repo = event["repo"]["name"]

    commit_count = event["payload"].get("size", 0)

    return f"{user} pushed {commit_count} commits to {repo}"

def handle_issues_event(event):
    user = event["actor"]["login"]
    repo = event["repo"]["name"]

    action = event["payload"]["action"]
    issue_number = event["payload"]["issue"]["number"]

    return f"{user} {action} issue #{issue_number} in {repo}"

def handle_unknown_event(event):
    user = event["actor"]["login"]
    repo = event["repo"]["name"]
    event_type = event["type"]

    return f"{user} performed {event_type} on {repo}"

def handle_pull_request_event(event):
    user = event["actor"]["login"]
    repo = event["repo"]["name"]
    action_status = event["payload"]["action"]

    return f"{user} {action_status} pull request on {repo}"

EVENT_HANDLERS = {
    "WatchEvent": handle_watch_event,
    "PushEvent": handle_push_event,
    "IssuesEvent": handle_issues_event,
    "PullRequestEvent": handle_pull_request_event
}



def format_events(events):
    if not events:
        return "⚠️ No events found!"
    
    user_events = []

    for event in events:
        event_type = event["type"]
        handler = EVENT_HANDLERS.get(event_type, handle_unknown_event)

        user_events.append(handler(event)) 

    return user_events




