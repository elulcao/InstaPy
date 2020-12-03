import unittest

from instapy import Settings


class TestSettings(unittest.TestCase):
    def test_log_location(self):
        assert Settings.log_location == None

    def test_database_location(self):
        assert Settings.database_location == None

    def test_user_agent(self):
        assert Settings.user_agent == None

    def test_profile(self):
        assert Settings.profile["id"] == None
        assert Settings.profile["name"] == None
