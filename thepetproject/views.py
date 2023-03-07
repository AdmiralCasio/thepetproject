from django.shortcuts import render
from django.http import HttpResponse
from thepetproject.models import UserProfile, Post, Comment
from django.contrib.auth.models import User


def index(request):
    return render(request, 'thepetproject/index.html')

def profile_page(request, username):
    context_dict = {}
    try:
        userprofile = UserProfile.objects.get(user=User.objects.get(username=username))
        posts = Post.objects.filter(user=userprofile).order_by('-date_posted').order_by('-time_posted')[:3]
        comments = Comment.objects.filter(user=userprofile).order_by('-likes')[:3]
        context_dict['userprofile'] = userprofile
        context_dict['recent_posts'] = posts
        context_dict['top_comments'] = comments
        
    except UserProfile.DoesNotExist:
        pass
    
    return render(request, 'thepetproject/profile_page.html', context=context_dict)
        
