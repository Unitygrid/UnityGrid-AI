import unittest
from ai_modules.text.text_generation import generate_text

class TestTextGeneration(unittest.TestCase):

    def test_generate_text(self):
        result = generate_text("Hello, world!")
        self.assertIn("Hello", result)

if __name__ == '__main__':
    unittest.main()
