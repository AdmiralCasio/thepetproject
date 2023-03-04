from django.contrib import admin
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedComment, UserHasLikedPost

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserHasLikedPost)
admin.site.register(UserHasLikedComment)
