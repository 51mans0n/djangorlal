import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.education.models import Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(email="u@test.com", password="12345")

@pytest.fixture
def auth_client(api_client, user):
    resp = api_client.post("/api/token/", {"email": "u@test.com", "password": "12345"}, format="json")
    assert resp.status_code == 200
    token = resp.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client

@pytest.mark.django_db
def test_courses_list_ok(auth_client, user):
    Course.objects.create(title="C1", owner=user)
    url = "/api/v1/education/courses/"
    resp = auth_client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) >= 1

@pytest.mark.django_db
def test_courses_list_unauth(api_client):
    url = "/api/v1/education/courses/"
    resp = api_client.get(url)
    assert resp.status_code == 401

@pytest.mark.django_db
def test_course_create_ok(auth_client):
    url = "/api/v1/education/courses/"
    resp = auth_client.post(url, {"title": "New course", "description": "Desc"}, format="json")
    assert resp.status_code == 201
    assert resp.data["title"] == "New course"

@pytest.mark.django_db
def test_course_create_bad_missing_title(auth_client):
    url = "/api/v1/education/courses/"
    resp = auth_client.post(url, {"description": "No title"}, format="json")
    assert resp.status_code == 400
