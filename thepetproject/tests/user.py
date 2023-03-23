from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib import auth
from django.urls import reverse

from thepetproject.models import UserProfile
from thepetproject.forms import UserForm, UserProfileForm


# The below was used thoroughly throughout the making of this file
# https://docs.djangoproject.com/en/4.1/topics/testing/
class UserTestCase(TestCase):
    def setUp(self):
        # Create one user in test DB
        self.username = "TestUser1"
        self.name = "Test User 1"
        self.password = "TestUserPassword"
        self.client = Client()

        user_data = {
            "username": self.username,
            "name": self.name,
            "password": self.password
            }

        user = UserForm(user_data).save()
        user.set_password("TestUserPassword")
        user.save()

        profile = UserProfileForm(user_data).save(commit=False)
        profile.user = user
        profile.date_joined = date.today()
        profile.save()

    def test_login(self):
        # Test login of user created in setUp()
        # Set up dict for login
        request_dict = {
            "username": self.username,
            "password": self.password
        }

        # Test client is not authenticated yet
        user = auth.get_user(self.client)
        self.assertTrue(not user.is_authenticated)

        # Login with test user created in setup
        self.client.post(reverse('thepetproject:login'), request_dict)

        # Test client is now authenticated
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        # Test logout of user created in setUp()
        # Set up dict for login
        request_dict = {
            "username": self.username,
            "password": self.password
        }

        # Login with test user created in setup
        self.client.post(reverse('thepetproject:login'), request_dict)

        # Test client is authenticated
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        # Logout client
        self.client.post(reverse('thepetproject:logout'), {})

        # Check client was logged out
        user = auth.get_user(self.client)
        self.assertTrue(not user.is_authenticated)

    def test_delete_user(self):
        # Test deletion of user created in setUp()
        # Login as test user
        request_dict = {
            "username": self.username,
            "password": self.password
        }
        self.client.post(reverse('thepetproject:login'), request_dict)

        # Delete the user
        self.client.post(reverse('thepetproject:myaccount'), {"type": "delete"})

        # Confirm user was deleted
        self.assertEqual(len(UserProfile.objects.all()), 0)


    def test_register(self):
        # Create new user, check they were created
        # Set up dict for register request
        request_dict = {
            "username": ["TestingUser"],
            "password": ["TestingPassword"],
            "name": ["Testing Name"],
            "picture": [""],
            "submit": ["Register"]
        }

        # Register user and check it was created
        self.client.post(reverse('thepetproject:sign-up'), request_dict)
        self.assertEqual(User.objects.all()[1].username, "TestingUser")

    def test_change_password(self):
        pass
