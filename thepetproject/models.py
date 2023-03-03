from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os

class UserProfile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    date_joined = models.DateField()
   
    def __str__(self):
        return self.user.username
    
    def get_correct_directory(self):
        return self.user.username
    
    picture = models.ImageField(blank = True, upload_to=get_correct_directory)
        
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_posted = models.DateField()
    time_posted = models.TimeField()
    likes = models.IntegerField(default=0)
    number_of_comments = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.post_id
    
    def get_correct_directory(self):
        return os.path.join(self.user.username, "/posts")
    
    image = models.ImageField(blank=False, upload_to=get_correct_directory)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    date_posted = models.DateField()
    time_posted = models.TimeField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment_id
    

    
