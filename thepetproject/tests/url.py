from os import path

from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse

from thepetproject.tests.test_utils import create_user, login_client, create_post, make_comment


# Tests to ensure URLs listed in url.py have endpoints
# The below doc was used thoroughly throughout the making of this file
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

    def test_index_endpoint(self):
        response = self.client.post(reverse("thepetproject:index"))

        # Expect 200 OK
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        response = self.client.post(reverse("thepetproject:login"), {"username": self.username, "password": self.password})

        # Expect 302 redirect
        self.assertEqual(response.status_code, 302)

    def test_logout_endpoint(self):
        login_client(self.username, self.password, self.client)

        response = self.client.post(reverse("thepetproject:logout"))
        # Expect 302 redirect
        self.assertEqual(response.status_code, 302)

    def test_register_endpoint(self):
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

    def test_upload_post_endpoint(self):
        response = create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect redirect
        self.assertEqual(response.status_code, 302)

        # login and try again
        login_client(self.username, self.password, self.client)
        response = create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect 200 OK
        self.assertEqual(response.status_code, 200)

    def test_view_posts_endpoint(self):
        response = self.client.post(reverse('thepetproject:view_posts'))

        # Expect 200 OK
        self.assertEqual(response.status_code, 200)

    def test_view_individual_post_endpoint(self):
        # Create the post and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:view_individual_post', kwargs={"post_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_like_post_endpoint(self):
        # Create the post to like and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:like_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_profile_endpoint(self):
        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:profile_page', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 200)

    def test_my_account_endpoint(self):
        # Login
        login_client(self.username, self.password, self.client)

        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:myaccount'))
        self.assertEqual(response.status_code, 200)

    def test_user_posts_endpoint(self):
        # Create the post to like and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:user_posts', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 200)

    def test_create_comment_endpoint(self):
        # Create the post and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Create comment, 302 redirect expected
        response = make_comment(self.client, "i like to comment")
        self.assertEqual(response.status_code, 200)

    def test_like_comment_endpoint(self):
        # Create the post and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Create comment
        make_comment(self.client, "i like to comment")

        # Like comment, expect 200 OK
        response = self.client.post(reverse("thepetproject:like_comment", kwargs={"post_id": 1, "comment_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_endpoint(self):
        # Create the post and login
        login_client(self.username, self.password, self.client)
        create_post(path.join(path.dirname(__file__), "cat.jpg"), 'this is a post', self.client)

        # Expect 200 OK
        response = self.client.post(reverse('thepetproject:delete_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)

