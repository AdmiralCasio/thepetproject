
from django import forms
from thepetproject.models import UserProfile, Comment
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


    text = forms.CharField(max_length = 1000, help_text="Your comment:")
    date_posted = forms.DateField(widget = forms.HiddenInput(), initial=date.today())
    time_posted = forms.TimeField(widget = forms.HiddenInput(), initial=datetime.now().time())

    class Meta:
        model = Comment
        fields = ('text', 'date_posted', 'time_posted')
