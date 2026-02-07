import unittest
from github_activity_cli.events_format import (
    format_events,
    handle_watch_event,
    handle_push_event,
    handle_issues_event,
    handle_pull_request_event,
    handle_unknown_event
)

class TestEventHandlers(unittest.TestCase):
    
    def test_handle_watch_event(self):
        event = {
            "type": "WatchEvent",
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"}
        }
        
        result = handle_watch_event(event)
        
        self.assertEqual(result, "testuser starred owner/repo")


    def test_handle_push_event(self):
        event = {
            "type": "PushEvent",
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"},
            "payload": {"size": 3}
        }
        
        result = handle_push_event(event)
        
        self.assertEqual(result, "testuser pushed 3 commits to owner/repo")

    def test_handle_push_event_no_commits(self):
        event = {
            "type": "PushEvent",
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"},
            "payload": {}  # No 'size' key
        }
        
        result = handle_push_event(event)
        
        self.assertEqual(result, "testuser pushed 0 commits to owner/repo")

    def test_handle_issues_event(self):
        event = {
            "type": "IssuesEvent",
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"},
            "payload": {
                "action": "opened",
                "issue": {"number": 42}
            }
        }
        
        result = handle_issues_event(event)
        
        self.assertEqual(result, "testuser opened issue #42 in owner/repo")
    
    def test_handle_pull_request_event(self):
        event = {
            "type": "PullRequestEvent",
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"},
            "payload": {"action": "opened"}
        }
        
        result = handle_pull_request_event(event)
        
        self.assertEqual(result, "testuser opened pull request on owner/repo")
    
    def test_handle_unknown_event(self):
        event = {
            "type": "CreateEvent",  
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"}
        }
        
        result = handle_unknown_event(event)
        
        self.assertEqual(result, "testuser performed CreateEvent on owner/repo")


if __name__ == "__main__":
    unittest.main() 