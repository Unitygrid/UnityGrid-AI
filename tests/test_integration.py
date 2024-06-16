import unittest
import pytest
from src.frontend.app import app, db

class TestIntegration(unittest.TestCase):

    def test_app(self):
        self.assertIsNotNone(app)
        self.assertIsNotNone(db)

if __name__ == '__main__':
    unittest.main()
