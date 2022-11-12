import pytest


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        first_name='Ivan',
        last_name='Ivanov',
        username='TestUser',
        email='ivanov@ivan.ru',
        password='12345'
    )
    return user


@pytest.fixture
def admin_user(django_user_model):
    user = django_user_model.objects.create_superuser(
        first_name='Vasiliy',
        last_name='Super',
        username='SuperUser',
        email='superuser@vasiliy.ru',
        password='12345'
    )
    return user


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def token_user(user):
    from rest_framework.authtoken.models import Token
    token = Token.objects.create(user=user)
    return {
        'auth_token': str(token),
    }


@pytest.fixture
def token_admin_user(admin_user):
    from rest_framework.authtoken.models import Token
    token = Token.objects.create(user=admin_user)
    return {
        'auth_token': str(token),
    }


@pytest.fixture
def auth_client(token_user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_user['auth_token']}")
    return client


@pytest.fixture
def admin_client(token_admin_user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_admin_user['auth_token']}")
    return client
