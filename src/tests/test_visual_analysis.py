import unittest
import pytest
from ai_modules.visual.visual_analysis import analyze_image


from src.ai_modules.visual.visual_analysis import predict

class TestVisualAnalysis(unittest.TestCase):

    def test_analyze_image(self):
        result = analyze_image("path/to/image.jpg")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()


def test_predict():
    image_path = 'src/tests/sample_image.jpg'
    with open(image_path, 'rb') as img:
        prediction = predict(img.read())
        assert prediction is not None
