from django.contrib.auth import get_user_model
from django.test import TestCase


# Create your tests here.

class UserModelTests(TestCase):
    """Tests for custom user model"""
    def test_create_user_with_email_successful(self):
        """Test creating new user with email is sucessful"""
        email='test@test.com'
        password='testtest'
        user = get_user_model().objects.create(
            email=email,
            password=password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
