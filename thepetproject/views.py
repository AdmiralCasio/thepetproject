from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from thepetproject.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UploadPostForm
from datetime import date,datetime

def index(request):

    post_list = Post.objects.order_by('-likes')[:3]
    context_dict = {}
    context_dict['posts'] = post_list
    return render(request, 'thepetproject/index.html', context=context_dict)

def profile_page(request, username=None):
    context_dict = {}
    try:
        if not username:
            if request.user.is_authenticated:
                username = request.user.username
                
        userprofile = UserProfile.objects.get(user=User.objects.get(username=username))
        posts = Post.objects.filter(user=userprofile).order_by('-date_posted').order_by('-time_posted')[:3]
        comments = Comment.objects.filter(user=userprofile).order_by('-likes')[:3]
        context_dict['userprofile'] = userprofile
        context_dict['recent_posts'] = posts
        context_dict['top_comments'] = comments
        
    except User.DoesNotExist:
        raise Http404(f"The user {str(username)} does not exist")
    
    return render(request, 'thepetproject/profile_page.html', context=context_dict)

def upload_post_page(request):
    submitted = False
    
    if request.method =="POST":
        form = UploadPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = UserProfile.objects.get(user = request.user)
            if 'image' in request.FILES:
                post.image=request.FILES['image']
            post.date_posted = date.today()
            post.time_posted = datetime.now().time()
            post.save()
            submitted=True
            return render(request, 'thepetproject/upload_post.html', {'form':form, 'submitted':submitted})
        else:
            print(form.errors)
        
    else:
        form = UploadPostForm

    return render(request, 'thepetproject/upload_post.html', {'form':form, 'submitted':submitted})