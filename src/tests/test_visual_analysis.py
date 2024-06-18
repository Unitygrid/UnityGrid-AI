import pytest
from src.ai_modules.visual.visual_analysis import analyze_image

def test_analyze_image():
    image_path = 'src/tests/sample_image.jpg'
    with open(image_path, 'rb') as img:
        prediction = analyze_image(img.read())
        assert prediction is not None