import pytest
from app import create_app

@pytest.fixture
def app():
    return create_app("Test")

@pytest.fixture
def test_client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    from app import db
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()