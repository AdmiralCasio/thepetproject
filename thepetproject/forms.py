from django import forms
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User

class UploadPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'image',)
        