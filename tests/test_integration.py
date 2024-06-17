import pytest
from src.frontend.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index(client):
    """Test the index page"""
    response = client.get('/')
    assert response.status_code == 200

def test_analyze_image(client):
    """Test image analysis endpoint"""
    image_path = 'src/tests/sample_image.jpg'
    with open(image_path, 'rb') as img:
        response = client.post('/analyze-image', data={'file': img})
        assert response.status_code == 200
        assert 'prediction' in response.get_json()

def test_generate_text(client):
    """Test text generation endpoint"""
    response = client.post('/generate-text', json={'prompt': 'Hello, world!'})
    assert response.status_code == 200
    assert 'text' in response.get_json()

def test_adios_task(client):
    """Test A.D.I.O.S. task endpoint"""
    response = client.post('/adios-task', json={'task': 'Schedule a meeting'})
    assert response.status_code == 200
    assert 'response' in response.get_json()
    assert 'task_id' in response.get_json()