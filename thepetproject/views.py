from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from thepetproject.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from thepetproject.forms import UserForm, UserProfileForm


def index(request):

    user_profile = None
    post_list = Post.objects.order_by('-likes')[:3]
    try:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        print("Error")
    context_dict = {}
    context_dict['posts'] = post_list
    context_dict['userprofile'] = user_profile
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
 
@login_required      
def my_account(request):
    user = User.objects.get(request.user)
    print(user.username)
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('thepetproject:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'thepetproject/login.html')

@login_required   
def user_logout(request):
    logout(request)
    return redirect(reverse('thepetproject:index'))

def register(request):
    registered = False
    
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.date_joined = date.today()
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'thepetproject/sign-up.html', {'user_form': user_form,
                                                   'profile_form': profile_form,
                                                   'registered': registered})
    
    
