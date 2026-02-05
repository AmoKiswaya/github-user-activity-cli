import unittest
from unittest.mock import patch, Mock, MagicMock
import json
from urllib.error import HTTPError, URLError

from github_activity_cli.git_api import fetch_user_events


class TestFetchUserEvents(unittest.TestCase):
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_success(self, mock_urlopen):
        """Test successful API call returns parsed JSON"""
        # Arrange: Create mock response data
        mock_events = [
            {
                "type": "PushEvent",
                "actor": {"login": "testuser"},
                "repo": {"name": "test/repo"},
                "payload": {"size": 3}
            }
        ]
        
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_events).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        mock_urlopen.return_value = mock_response
        
        # Act: Call the function
        result = fetch_user_events("testuser")
        
        # Assert: Check the result
        self.assertEqual(result, mock_events)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "PushEvent")
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_not_found(self, mock_urlopen):
        """Test 404 error raises ValueError"""
        # Arrange: Create mock 404 error
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/nonexistent/events",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        
        # Act & Assert: Check that ValueError is raised
        with self.assertRaises(ValueError) as context:
            fetch_user_events("nonexistent")
        
        self.assertEqual(str(context.exception), "User not found")
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_rate_limit(self, mock_urlopen):
        """Test 403 rate limit error with reset time"""
        # Arrange: Create mock 403 error with rate limit headers
        mock_error = HTTPError(
            url="https://api.github.com/users/testuser/events",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None
        )
        mock_error.headers = Mock()
        mock_error.headers.get = Mock(side_effect=lambda key: {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1704067200"  # Some timestamp
        }.get(key))
        
        mock_urlopen.side_effect = mock_error
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            fetch_user_events("testuser")
        
        self.assertIn("Rate limit exceeded", str(context.exception))
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_403_without_rate_limit(self, mock_urlopen):
        """Test 403 error without rate limit headers"""
        # Arrange
        mock_error = HTTPError(
            url="https://api.github.com/users/testuser/events",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None
        )
        mock_error.headers = Mock()
        mock_error.headers.get = Mock(return_value=None)
        
        mock_urlopen.side_effect = mock_error
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            fetch_user_events("testuser")
        
        self.assertEqual(str(context.exception), "Access forbidden by GitHub")
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_network_error(self, mock_urlopen):
        """Test network error raises RuntimeError"""
        # Arrange
        mock_urlopen.side_effect = URLError("Connection refused")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            fetch_user_events("testuser")
        
        self.assertIn("Network error", str(context.exception))
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_other_http_error(self, mock_urlopen):
        """Test other HTTP errors (e.g., 500)"""
        # Arrange
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/testuser/events",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            fetch_user_events("testuser")
        
        self.assertIn("GitHub API error 500", str(context.exception))
    
    @patch('github_activity_cli.git_api.urllib.request.urlopen')
    def test_fetch_user_events_empty_response(self, mock_urlopen):
        """Test empty events list"""
        # Arrange
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps([]).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        mock_urlopen.return_value = mock_response
        
        # Act
        result = fetch_user_events("testuser")
        
        # Assert
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()