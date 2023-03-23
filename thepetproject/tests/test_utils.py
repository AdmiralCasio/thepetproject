from datetime import date

from thepetproject.forms import UserForm, UserProfileForm
from django.test import Client
from django.urls import reverse


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


def login_client(username, password, client: Client) -> Client:
    user_data = {"username": username, "password": password}
    client.post(reverse('thepetproject:login'), user_data)
    return client
