from django import forms
from django.forms import ModelForm
from thepetproject.models import UserProfile, Comment, Post
from django.contrib.auth.models import User
from datetime import datetime, date


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'picture')
        
class ChangeProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )

class CreateCommentForm(forms.ModelForm):
    #code for date found at: https://www.geeksforgeeks.org/datefield-django-models/
    #code for time found at: https://www.geeksforgeeks.org/timefield-django-models/
    #code for default time found at: https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time


    text = forms.CharField(max_length = 1000, help_text="Your comment:")
    date_posted = forms.DateField(widget = forms.HiddenInput(), initial=date.today())
    time_posted = forms.TimeField(widget = forms.HiddenInput(), initial=datetime.now().time())

    class Meta:
        model = Comment
        fields = ('text', 'date_posted', 'time_posted')
        
class UploadPostForm(forms.ModelForm):
    #code for adding id to form elements found at: https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    caption=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = ('image', 'caption',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['caption'].widget.attrs.update({'id':'caption-style'})
        self.fields['image'].widget.attrs.update({'id':'image-style'})