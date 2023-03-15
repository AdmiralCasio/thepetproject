from django import forms
from thepetproject.models import Comment

class CreateCommentForm(forms.ModelForm):
      pass
#     text = forms.CharField(max_length = 1000, help_text="Your comment goes here...")
#     likes = forms.IntegerField(widget = forms.HiddenInput(), intial = 0)
#     date_posted = forms.DateField(widget = forms.HiddenInput())
#     time_posted = forms.TimeField(widget = forms.HiddenInput())
#
#     class Meta:
#         model = Comment
#         fields = ('text',)
