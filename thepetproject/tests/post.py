from datetime import date
from os import path
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from thepetproject.forms import UserForm, UserProfileForm
from thepetproject.models import Post, Comment, User


# The below docs were used thoroughly throughout the making of this file
# https://docs.djangoproject.com/en/4.1/topics/testing/
class PostTestCase(TestCase):
    def setUp(self):
        # Create one user and log client in
        self.username = "TestUser1"
        self.name = "Test User 1"
        self.password = "TestUserPassword"
        self.client = Client()

        # Create user
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

        # Login to user
        user_data.pop("name")
        self.client.post(reverse('thepetproject:login'), user_data)

    def test_create_post(self):
        # Prep dict
        with open(path.join(path.dirname(__file__), "cat.jpg"), 'rb') as file:
            image = file.read()

        post_dict = {
            "caption": ['this is a post'],
            "image": [SimpleUploadedFile("cat.jpg", image, content_type="image/jpeg")]
        }

        # Create post
        self.client.post(reverse('thepetproject:upload_post_page'), post_dict)

        # Check post was created
        self.assertEqual(len(Post.objects.all()), 1)

    def test_delete_post(self):
        # Create post
        self.test_create_post()

        # Try to delete post
        self.client.post(reverse("thepetproject:delete_post", kwargs={'post_id': str(Post.objects.all()[0].post_id)}))

        # Check post was deleted
        self.assertEqual(len(Post.objects.all()), 0)

    def test_like_post(self):
        # Create post
        self.test_create_post()

        # Check theres no likes
        self.assertEqual(Post.objects.all()[0].likes, 0)

        # Like the post
        self.client.post(reverse("thepetproject:like_post", kwargs={'post_id': str(Post.objects.all()[0].post_id)}))

        # Check there is now 1 like
        self.assertEqual(Post.objects.all()[0].likes, 1)

    def test_unlike_post(self):
        # Create post, like post
        self.test_like_post()

        # Unlike post, the function to like the post is the same to unlike it
        self.client.post(reverse("thepetproject:like_post", kwargs={'post_id': str(Post.objects.all()[0].post_id)}))

        # Check likes there are now 0 likes
        self.assertEqual(Post.objects.all()[0].likes, 0)

    def test_comment_on_post(self):
        # Create post
        self.test_create_post()

        # Check there are no comments
        self.assertEqual(len(Comment.objects.all()), 0)

        # Make comment
        self.client.post(reverse("thepetproject:create_comment", kwargs={'post_id': str(Post.objects.all()[0].post_id)}), {
                "time_posted": ["10:10:10.123456"],
                "date_posted": ["2023-03-23"],
                "text": ["i am a comment :)"],
                "create_comment": ['Create Comment']
        })

        # Check there is now 1 comment
        self.assertEqual(Comment.objects.get(post_id=str(Post.objects.all()[0].post_id)).text, "i am a comment :)")

    def test_like_comment_on_post(self):
        # Create post, comment on post
        self.test_comment_on_post()
        post_id = Post.objects.all()[0].post_id

        # Check post has no likes
        self.assertEqual(Comment.objects.get(post_id=post_id).likes, 0)

        # Like post
        self.client.post(reverse("thepetproject:like_comment", kwargs={
            "post_id": str(post_id),
            "comment_id": str(Comment.objects.get(post_id=post_id).comment_id)
            })
        )

        # Check post has 1 like
        self.assertEqual(Comment.objects.get(post_id=post_id).likes, 1)

    def test_unlike_comment_on_post(self):
        # Create post, comment on post, like post
        self.test_like_comment_on_post()
        post_id = Post.objects.all()[0].post_id

        # Unlike post
        self.client.post(reverse("thepetproject:like_comment", kwargs={
            "post_id": str(post_id),
            "comment_id": str(Comment.objects.get(post_id=post_id).comment_id)
            })
        )

        # Check post has no likes
        self.assertEqual(Comment.objects.get(post_id=post_id).likes, 0)
