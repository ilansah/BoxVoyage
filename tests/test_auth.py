import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.auth import Users, AuthManager
from data.storage import JsonStorage


class TestAuthBasic(unittest.TestCase):
    """Basic authentication tests."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.write('{}')
        self.temp_file.close()
        self.storage = JsonStorage(self.temp_file.name)
        self.auth = AuthManager(self.storage)
    
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
    
    def test_create_user(self):
        """Test creating and registering a user."""
        user = self.auth.register("alice", "password123")
        self.assertEqual(user.username, "alice")
    
    def test_authenticate_user(self):
        """Test authenticating a user."""
        self.auth.register("alice", "password123")
        user = self.auth.login("alice", "password123")
        self.assertEqual(user.username, "alice")
        self.assertEqual(self.auth.get_current_user().username, "alice")
    
    def test_wrong_password(self):
        """Test authentication fails with wrong password."""
        self.auth.register("alice", "password123")
        with self.assertRaises(ValueError):
            self.auth.login("alice", "wrong_password")
    
    def test_logout(self):
        """Test logout clears current user."""
        self.auth.register("alice", "password123")
        self.auth.login("alice", "password123")
        self.auth.logout()
        self.assertIsNone(self.auth.get_current_user())


if __name__ == "__main__":
    unittest.main()
