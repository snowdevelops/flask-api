import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'

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

def test_register_duplicate_email(client):
    client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secret123'
    })
    response = client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secret123'
    })
    data = response.get_json()

    assert response.status_code == 409
    assert data['success'] ==  False

def test_login_success(client):
    client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secret123'
    })

    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'secret123'
    })
    data = response.get_json()

    assert response.status_code == 200
    assert data['success'] == True
    assert 'token' in data['data']

def test_login_wrong_password(client):
    client.post('auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secret123'
    })
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    data = response.get_json()

    assert response.status_code == 401
    assert data['success'] == False
