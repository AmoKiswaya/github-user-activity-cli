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


class TestFormatEvents(unittest.TestCase):
    """Test the main format_events function"""
    
    def test_format_events_empty_list(self):
        result = format_events([])
        
        self.assertEqual(result, ["No recent activity found!"])
    
    def test_format_events_single_push(self):
        events = [{
            "type": "PushEvent",
            "actor": {"login": "alice"},
            "repo": {"name": "alice/project"},
            "payload": {"size": 2}
        }]
        
        result = format_events(events)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "alice pushed 2 commits to alice/project")
    
    def test_format_events_multiple_types(self):
        events = [
            {
                "type": "PushEvent",
                "actor": {"login": "alice"},
                "repo": {"name": "alice/project"},
                "payload": {"size": 1}
            },
            {
                "type": "WatchEvent",
                "actor": {"login": "bob"},
                "repo": {"name": "alice/project"}
            },
            {
                "type": "IssuesEvent",
                "actor": {"login": "charlie"},
                "repo": {"name": "owner/repo"},
                "payload": {
                    "action": "closed",
                    "issue": {"number": 10}
                }
            }
        ]
        
        result = format_events(events)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "alice pushed 1 commits to alice/project")
        self.assertEqual(result[1], "bob starred alice/project")
        self.assertEqual(result[2], "charlie closed issue #10 in owner/repo")
    
    def test_format_events_with_unknown_type(self):
        events = [{
            "type": "ForkEvent",  # Not in EVENT_HANDLERS
            "actor": {"login": "testuser"},
            "repo": {"name": "owner/repo"}
        }]
        
        result = format_events(events)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "testuser performed ForkEvent on owner/repo")
    
    def test_format_events_preserves_order(self):
        """Test that events are formatted in the same order"""
        events = [
            {
                "type": "PushEvent",
                "actor": {"login": "user1"},
                "repo": {"name": "repo1"},
                "payload": {"size": 1}
            },
            {
                "type": "PushEvent",
                "actor": {"login": "user2"},
                "repo": {"name": "repo2"},
                "payload": {"size": 2}
            },
            {
                "type": "PushEvent",
                "actor": {"login": "user3"},
                "repo": {"name": "repo3"},
                "payload": {"size": 3}
            }
        ]
        
        result = format_events(events)
        
        self.assertIn("user1", result[0])
        self.assertIn("user2", result[1])
        self.assertIn("user3", result[2])


if __name__ == "__main__":
    unittest.main() 