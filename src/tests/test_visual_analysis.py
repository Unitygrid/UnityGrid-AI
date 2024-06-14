import unittest
from ai_modules.visual_analysis import analyze_image

class TestVisualAnalysis(unittest.TestCase):

    def test_analyze_image(self):
        result = analyze_image("path/to/image.jpg")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
