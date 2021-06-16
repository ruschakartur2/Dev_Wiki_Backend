from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# Create your tests here.
from django.urls import reverse

CREATE_USER_URL = reverse('create')
TOKEN_USER_URL = reverse('login')
ME_URL = reverse('me')


def create_user(**params):
    """Function to create user"""
    return get_user_model().objects.create_user(**params)


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
            'email': 'test123@test.com',
            'password': 'fhnehheofr555605',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test create user that already exists fails"""
        payload = {
            'email': 'test123@test.com',
            'password': 'fhnehheofr555605',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_short_password(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'test@test.com',
            'password': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if user credentials is invalid"""
        payload = {
            'email': 'test@test.com',
            'password': 'invalid'
        }
        create_user(email='test@test.com', password='testtest')

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not created if user doesn't exists"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_USER_URL, {'email': 'test',
                                                'password': ''})

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)