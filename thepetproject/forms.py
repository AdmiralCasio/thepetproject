from django import forms
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User

class UploadPostForm(forms.ModelForm):

    caption=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = ('image', 'caption',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['caption'].widget.attrs.update({'id':'caption-style'})
        self.fields['image'].widget.attrs.update({'id':'image-style'})


        