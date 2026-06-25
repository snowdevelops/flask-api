import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register_and_login(client, email, name='User'):
    client.post('/auth/register', json={
        'name': name,
        'email': email,
        'password': 'secret123'
    })
    res = client.post('/auth/login', json={
        'email': email,
        'password': 'secret123'
    })
    return res.get_json()['data']['token']


def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


# --- User authorization ---

def test_user_can_update_own_account(client):
    token = register_and_login(client, 'alice@example.com', 'Alice')
    res = client.put('/users/1', json={'name': 'Alice Updated'}, headers=auth_header(token))
    assert res.status_code == 200


def test_user_cannot_update_another_account(client):
    token_alice = register_and_login(client, 'alice@example.com', 'Alice')
    register_and_login(client, 'bob@example.com', 'Bob')

    res = client.put('/users/2', json={'name': 'Hacked'}, headers=auth_header(token_alice))
    assert res.status_code == 403
    assert res.get_json()['success'] == False


def test_user_can_delete_own_account(client):
    token = register_and_login(client, 'alice@example.com', 'Alice')
    res = client.delete('/users/1', headers=auth_header(token))
    assert res.status_code == 200


def test_user_cannot_delete_another_account(client):
    token_alice = register_and_login(client, 'alice@example.com', 'Alice')
    register_and_login(client, 'bob@example.com', 'Bob')

    res = client.delete('/users/2', headers=auth_header(token_alice))
    assert res.status_code == 403
    assert res.get_json()['success'] == False


# --- Post authorization ---

def test_user_can_update_own_post(client):
    token = register_and_login(client, 'alice@example.com', 'Alice')
    client.post('/posts', json={'title': 'My Post', 'body': 'Hello', 'user_id': 1})
    res = client.put('/posts/1', json={'title': 'Updated'}, headers=auth_header(token))
    assert res.status_code == 200


def test_user_cannot_update_another_users_post(client):
    token_alice = register_and_login(client, 'alice@example.com', 'Alice')
    token_bob = register_and_login(client, 'bob@example.com', 'Bob')

    client.post('/posts', json={'title': 'Alice Post', 'body': 'Hello', 'user_id': 1})
    res = client.put('/posts/1', json={'title': 'Hijacked'}, headers=auth_header(token_bob))
    assert res.status_code == 403


def test_user_can_delete_own_post(client):
    token = register_and_login(client, 'alice@example.com', 'Alice')
    client.post('/posts', json={'title': 'My Post', 'body': 'Hello', 'user_id': 1})
    res = client.delete('/posts/1', headers=auth_header(token))
    assert res.status_code == 200


def test_user_cannot_delete_another_users_post(client):
    token_alice = register_and_login(client, 'alice@example.com', 'Alice')
    token_bob = register_and_login(client, 'bob@example.com', 'Bob')

    client.post('/posts', json={'title': 'Alice Post', 'body': 'Hello', 'user_id': 1})
    res = client.delete('/posts/1', headers=auth_header(token_bob))
    assert res.status_code == 403
