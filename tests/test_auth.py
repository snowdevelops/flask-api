import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory',
        'JWT_SECRET_KEY': 'test-secret'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_success(client):
    response = client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secret123'
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data['data']['email'] == 'test@example.com'
    assert data ['data']['name'] == 'Test User'