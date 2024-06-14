import pytest
python
from frontend.app import app, db
from config import test_config

@pytest.fixture
def client():
    app.config.from_object(test_config)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
