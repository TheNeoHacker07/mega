from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.user.serializer import UserRegisterSerializer, UserLoginSerializer

User = get_user_model()


class UserSerializersTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="existing@example.com",
            password="password123"
        )

    def test_register_serializer_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "strongpass1",
            "password_confirm": "strongpass1"
        }

        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("strongpass1"))

    def test_register_serializer_password_mismatch(self):
        data = {
            "email": "newuser@example.com",
            "password": "strongpass1",
            "password_confirm": "strongpass2"
        }

        serializer = UserRegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("PASSWORDS DIDNT MATCH", str(serializer.errors))

    def test_register_serializer_existing_email(self):
        data = {
            "email": "existing@example.com",
            "password": "password123",
            "password_confirm": "password123"
        }

        serializer = UserRegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("USER ALREADY EXISTS", str(serializer.errors))

    def test_login_serializer_success(self):
        data = {
            "email": "existing@example.com",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"].email, "existing@example.com")

    def test_login_serializer_wrong_password(self):
        data = {
            "email": "existing@example.com",
            "password": "wrongpassword"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("invalid email or password", str(serializer.errors))

    def test_login_serializer_user_not_found(self):
        data = {
            "email": "nouser@example.com",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("user not found", str(serializer.errors))


class UserAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.register_url = reverse("user-register-list")
        self.login_url = reverse("user-login-list")

        self.user_data = {
            "email": "testuser@example.com",
            "password": "password123",
            "password_confirm": "password123"
        }

        self.existing_user = User.objects.create_user(
            email="existing@example.com",
            password="password123"
        )

    def test_register_api_success(self):
        response = self.client.post(self.register_url, data=self.user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_register_api_existing_email(self):
        data = {
            "email": "existing@example.com",
            "password": "password123",
            "password_confirm": "password123"
        }

        response = self.client.post(self.register_url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("USER ALREADY EXISTS", str(response.data))

    def test_login_api_success(self):
        data = {
            "email": "existing@example.com",
            "password": "password123"
        }

        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_api_wrong_password(self):
        data = {
            "email": "existing@example.com",
            "password": "wrongpass"
        }

        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid email or password", str(response.data))

    def test_login_api_user_not_found(self):
        data = {
            "email": "nouser@example.com",
            "password": "password123"
        }

        response = self.client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("user not found", str(response.data))