import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_view(client):
    url = reverse("users:register")
    response = client.get(url)
    assert response.status_code == 200
    assert "users/register.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_email_verification(client, user):
    user.token = "testtoken"
    user.save()

    url = reverse("users:confirm-registration", kwargs={"token": "testtoken"})
    response = client.get(url)

    user.refresh_from_db()
    assert user.is_active is True
    assert response.status_code == 302  # редирект на login


@pytest.mark.django_db
def test_login_view(client, user):
    url = reverse("users:login")
    response = client.get(url)
    assert response.status_code == 200
    assert "users/login.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_profile_view(client, user):
    client.force_login(user)
    url = reverse("users:profile", kwargs={"pk": user.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert "users/profile.html" in [t.name for t in response.templates]
    assert response.context["object"] == user


@pytest.mark.django_db
def test_edit_profile_view(client, user):
    client.force_login(user)
    url = reverse("users:edit_profile")
    response = client.get(url)

    assert response.status_code == 200
    assert "users/edit_profile.html" in [t.name for t in response.templates]
