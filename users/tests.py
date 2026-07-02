import pytest
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
@pytest.mark.django_db
def test_login_page_opens(client):
    response = client.get(reverse("users:login"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_register_page_opens(client):
    response = client.get(reverse("users:register"))

    assert response.status_code == 200