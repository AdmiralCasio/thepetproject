from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedPost, UserHasLikedComment

from thepetproject.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse

from thepetproject.forms import CreateCommentForm


def index(request):
    return render(request, 'thepetproject/index.html')

def like_comment(request, post_id, comment_id):
    # JsonResponse found at: https://docs.djangoproject.com/en/4.1/ref/request-response/
    user_profile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(post_id=post_id)
    comment = Comment.objects.get(comment_id=comment_id)
    user_likes_comment_instance = UserHasLikedComment.objects.get_or_create(comment=comment, user=user_profile)
    if user_likes_comment_instance[1]:
        comment.likes += 1
        comment.save()

    response = {"likes": str(post.likes)}
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
        comment = "none"
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
                    'user_profile': user_profile,
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
    url = 'thepetproject/create_comment.html'
    return render(request, url, context=context_dict)

def add_comment(request, post_id):

    # form = CreateCommentForm()

    url = "thepetproject/view_individual_post.html"
    context_dict = get_view_post_context_dict(request)
    return render(request, url, context=context_dict)

def profile_page(request, username):
    context_dict = {}
    try:
        if not username:
            if request.user:
                username = request.user
            else:
                return redirect(reverse('thepetproject:index'))
        userprofile = UserProfile.objects.get(user=User.objects.get(username=username))
        posts = Post.objects.filter(user=userprofile).order_by('-date_posted').order_by('-time_posted')[:3]
        comments = Comment.objects.filter(user=userprofile).order_by('-likes')[:3]
        context_dict['userprofile'] = userprofile
        context_dict['recent_posts'] = posts
        context_dict['top_comments'] = comments
        
    except UserProfile.DoesNotExist:
        pass
    
    return render(request, 'thepetproject/profile_page.html', context=context_dict)

