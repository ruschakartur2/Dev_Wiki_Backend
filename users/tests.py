from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# Create your tests here.
from django.urls import reverse

CREATE_USER_URL = reverse('users:registration')


class UserModelTests(TestCase):
    """Tests for custom user model"""

    def test_create_user_with_email_successful(self):
        """Test creating new user with email is sucessful"""
        email = 'test@test.com'
        password = 'testtest'
        user = get_user_model().objects.create(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertFalse(user.check_password(password))


class PublicUserAPITests(TestCase):
    """Test the users API(public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password1': 'fhnehheofr555605',
            'password2': 'fhnehheofr555605'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertFalse(user.check_password(payload['password1']))
        self.assertNotIn('password1', res.data)
