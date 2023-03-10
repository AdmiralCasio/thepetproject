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
    
    def get_correct_directory(self, filename):
        return os.path.join(self.user.username, filename)
    
    picture = models.ImageField(blank = True, upload_to=get_correct_directory)
        
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=500)
    
    def get_correct_directory(self, filename):
        return os.path.join(self.user.user.username, 'posts', filename)
    
    image = models.ImageField(blank=False, upload_to=get_correct_directory, default='default-profile.jpg')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_posted = models.DateField()
    time_posted = models.TimeField()
    likes = models.IntegerField(default=0)
    number_of_comments = models.IntegerField(default=0)
    
    
    def __str__(self):
        return str(self.post_id)
    
    
    #image = models.ImageField(blank=False, upload_to='media/')

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    date_posted = models.DateField()
    time_posted = models.TimeField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.comment_id)
    
    
class UserHasLikedPost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) + " " + str(self.post)
    
class UserHasLikedComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) + " " + str(self.comment)

    
