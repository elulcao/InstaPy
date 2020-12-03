import unittest

from instapy import util


class TestsActionDelay(unittest.TestCase):
    def test_default_values_returned(self):
        assert util.get_action_delay("like") == 2
        assert util.get_action_delay("comment") == 2
        assert util.get_action_delay("follow") == 3
        assert util.get_action_delay("unfollow") == 10
