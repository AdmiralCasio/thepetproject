from django.test import TestCase, Client
from django.urls import reverse

from thepetproject.tests.test_utils import create_user, login_client


# Tests to ensure URLs have end points
# The below docs were used thoroughly throughout the making of this file
# https://docs.djangoproject.com/en/4.1/topics/testing/
class UrlEndpointsTestCase(TestCase):
    def setUp(self):
        # Create one user and log client in
        self.username = "TestUser1"
        self.name = "Test User 1"
        self.password = "TestUserPassword"
        self.client = Client()

        # Create user
        create_user(self.username, self.name, self.password)

    def test_index(self):
        response = self.client.post(reverse("thepetproject:index"))

        # Expect 200 OK
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse("thepetproject:login"), {"username": self.username, "password": self.password})

        # Expect 302 redirect
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        login_client(self.username, self.password, self.client)

        response = self.client.post(reverse("thepetproject:logout"))
        # Expect 302 redirect
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        request_dict = {
            "username": ["TestingUser"],
            "password": ["TestingPassword"],
            "name": ["Testing Name"],
            "picture": [""],
            "submit": ["Register"]
        }

        response = self.client.post(reverse('thepetproject:sign-up'), request_dict)
        # Expect 200 OK
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        pass

    def test_view_posts(self):
        pass

    def test_view_individual_post(self):
        pass

    def test_like_post(self):
        pass

    def test_profile(self):
        pass

    def test_my_account(self):
        pass

    def test_user_posts(self):
        pass

    def test_create_comment(self):
        pass

    def test_like_comment(self):
        pass

    def test_delete_post(self):
        pass

