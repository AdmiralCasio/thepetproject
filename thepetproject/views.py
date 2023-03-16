
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedPost, UserHasLikedComment
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from thepetproject.forms import UserForm, UserProfileForm, ChangeProfilePictureForm, CreateCommentForm
import os
from django.conf import settings

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

def like_comment(request, post_id, comment_id):
    # JsonResponse found at: https://docs.djangoproject.com/en/4.1/ref/request-response/
    user_profile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(post_id=post_id)
    comment = Comment.objects.get(comment_id=comment_id)
    user_likes_comment_instance = UserHasLikedComment.objects.get_or_create(comment=comment, user=user_profile)
    if user_likes_comment_instance[1]:
        comment.likes += 1
        comment.save()

    response = {"likes": str(comment.likes)}
    return JsonResponse(response)

def like_post(request, post_id):
    #JsonResponse found at: https://docs.djangoproject.com/en/4.1/ref/request-response/
    user_profile = UserProfile.objects.get(user = request.user)
    post = Post.objects.get(post_id=post_id)
    user_likes_post_instance = UserHasLikedPost.objects.get_or_create(post = post, user = user_profile)
    if user_likes_post_instance[1]:
        post.likes += 1
        post.save()
    response = {"likes": str(post.likes)}
    return JsonResponse(response)

def get_view_post_context_dict(request, post_id):

    post = Post.objects.get(post_id=post_id)
    post_user = UserProfile.objects.get(user_id = post.user_id)
    try:
        comment = Comment.objects.filter(post_id = post_id).order_by('-date_posted').order_by('-time_posted')[0]
    except:
        comment = None
    current_user = request.user
    user_profile = UserProfile.objects.get(user = current_user)
    try:
        has_user_liked_post = UserHasLikedPost.objects.get(user = user_profile, post = post)
    except UserHasLikedPost.DoesNotExist:
        has_user_liked_post = False
    else:
        has_user_liked_post = True
    try:
        has_user_liked_comment = UserHasLikedComment.objects.get(user = user_profile, comment = comment)
    except UserHasLikedComment.DoesNotExist:
        has_user_liked_comment = False
    else:
        has_user_liked_comment = True

    context_dict = {'post': post, 'comment': comment, 'user': current_user, 'post_user': post_user,
                    'userprofile': user_profile,
                    'user_has_liked_post': has_user_liked_post,
                    'user_has_liked_comment': has_user_liked_comment}

    return context_dict
def view_individual_post(request, post_id):

    context_dict = get_view_post_context_dict(request, post_id)

    url = 'thepetproject/view_individual_post.html'
    return render(request, url , context = context_dict)

def create_comment(request, post_id):

    post = Post.objects.get(post_id = post_id)
    context_dict = {'post': post}

    if request.method == "POST":
        form = CreateCommentForm(request.POST)
    else:
        form = CreateCommentForm()
    context_dict['form'] = form

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_id = post_id
        current_user = UserProfile.objects.get(user = request.user)
        comment.user = current_user
        comment.save()
        url = "thepetproject/view_individual_post.html"
        context_dict = get_view_post_context_dict(request, post_id)
        return render(request, url, context=context_dict)
    else:
        print(form.errors)

    url = 'thepetproject/create_comment.html'
    return render(request, url, context=context_dict)


def profile_page(request, username=None):
    context_dict = {'user_exists':True}
    userprofile = None
    if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user=request.user)
    context_dict['userprofile'] = userprofile
    try:
        if not username:
            if request.user.is_authenticated:
                username = request.user.username
        
        userprofile_page = UserProfile.objects.get(user=User.objects.get(username=username))
        posts = Post.objects.filter(user=userprofile_page).order_by('-date_posted', '-time_posted')[:3]
        comments = Comment.objects.filter(user=userprofile_page).order_by('-likes')[:3]
        
        context_dict['userprofile_page'] = userprofile_page
        context_dict['recent_posts'] = posts
        context_dict['top_comments'] = comments
        
    except User.DoesNotExist:
        context_dict['user_exists'] = False
            
    return render(request, 'thepetproject/profile_page.html', context=context_dict)

 
@login_required      
def my_account(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        image_path_list = user.picture.path.split('\\')
        context_dict = {'userprofile':user}
        if request.method == "POST":
            if request.POST.get('type') == None:
                form = ChangeProfilePictureForm(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    image_path = os.path.join(settings.MEDIA_DIR, user.user.username, image_path_list[-1])
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    form.save()
                else:
                    print(form.errors)
            elif request.POST.get('type') == 'password':
                user.user.set_password(request.POST.get('password'))
                user.user.save()
                return HttpResponse({'status':1})
            elif request.POST.get('type') == 'name':
                user.name = request.POST.get('name')
                user.save()
                return HttpResponse({'status':1}) 
            elif request.POST.get('type') == 'delete':
                print("Deleting...")
                User.objects.get(username=request.user.username).delete()
                print("Deleted")
                
        else:
            form = ChangeProfilePictureForm()

            context_dict['profilepictureform'] = form
            
        
        return render(request, 'thepetproject/my-account.html', context=context_dict)
    except:
        return redirect(reverse('thepetproject:index'))
                
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
            return HttpResponse("Invalid login details supplied. <a href=" + reverse("thepetproject:login") + ">Go back</a>")
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
