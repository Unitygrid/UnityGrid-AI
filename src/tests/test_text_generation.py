from src.ai_modules.text_generation import generate_text

def test_generate_text():
    assert generate_text() == "Text generated"
