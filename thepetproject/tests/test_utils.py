from datetime import date

from thepetproject.forms import UserForm, UserProfileForm
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


# A file to hold functions used in different tests
# The below docs were used thoroughly throughout the making of this file
# https://docs.djangoproject.com/en/4.1/topics/testing/
def create_user(username, name, password):
    user_data = {
        "username": username,
        "name": name,
        "password": password
    }

    user = UserForm(user_data).save()
    user.set_password("TestUserPassword")
    user.save()

    profile = UserProfileForm(user_data).save(commit=False)
    profile.user = user
    profile.date_joined = date.today()
    profile.save()


def create_post(image_path, caption, client: Client):
    # Prep dict
    with open(image_path, 'rb') as file:
        image = file.read()

    post_dict = {
        "caption": [caption],
        "image": [SimpleUploadedFile("cat.jpg", image, content_type="image/jpeg")]
    }

    # Create post
    client.post(reverse('thepetproject:upload_post_page'), post_dict)


def login_client(username, password, client: Client) -> Client:
    user_data = {"username": username, "password": password}
    client.post(reverse('thepetproject:login'), user_data)
    return client
