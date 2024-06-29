import pytest
from src.ai_modules.visual.visual_analysis import analyze_image

def test_analyze_image():
    image_path = 'src/tests/sample_image.jpg'
    assert os.path.exists(image_path), f"Image file not found: {image_path}"
    with open(image_path, 'rb') as img:
        image_bytes = img.read()
    result = analyze_image(image_bytes)
    assert result is not None