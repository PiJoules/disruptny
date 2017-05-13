from server import *
import unittest
import server
import urllib
from flask import json, url_for


class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def test_empty_targets(self):
        r = self.app.get("/broadcast_custom")
        self.assertEqual(
            json.loads(r.data),
            EmptyTargets().__dict__
        )

    def test_empty_message(self):
        r = self.app.get("/broadcast_custom", query_string={
            "targets": [FAKE_NUMBER, FAKE_NUMBER],
            "msg": "   "
        })
        self.assertEqual(
            json.loads(r.data),
            EmptyMessage().__dict__
        )

    def test_success(self):
        r = self.app.get("/broadcast_custom", query_string={
            "targets": [FAKE_NUMBER, FAKE_NUMBER],
            "msg": "Some msg"
        })
        self.assertEqual(
            json.loads(r.data),
            Success().__dict__
        )


if __name__ == "__main__":
    unittest.main()
