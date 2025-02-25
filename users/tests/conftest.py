import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(email="test@example.com", password="testpassword")

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(email="admin@example.com", password="adminpassword")

@pytest.fixture
def client(db):
    """Фикстура для клиента, который делает запросы"""
    from django.test import Client
    return Client()
