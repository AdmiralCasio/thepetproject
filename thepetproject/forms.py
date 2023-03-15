
from datetime import datetime, date

from django import forms
from thepetproject.models import Comment

class CreateCommentForm(forms.ModelForm):
    #code for date found at: https://www.geeksforgeeks.org/datefield-django-models/
    #code for time found at: https://www.geeksforgeeks.org/timefield-django-models/


    text = forms.CharField(max_length = 1000, help_text="Your comment:")
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
    date_posted = forms.DateField(widget = forms.HiddenInput(), initial=date.today())
    time_posted = forms.TimeField(widget = forms.HiddenInput(), initial=datetime.now())

    class Meta:
        model = Comment
        fields = ('text', 'likes', 'date_posted', 'time_posted')
