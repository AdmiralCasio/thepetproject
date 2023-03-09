from django.shortcuts import render, redirect
from django.http import HttpResponse
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedPost, UserHasLikedComment

from thepetproject.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse


def index(request):
    return render(request, 'thepetproject/index.html')

def like(request):
    comment_or_post_id = request.GET['comment_or_post_id']
    isPost = request.get['isPost']
    if isPost:
        post = Post.get(comment_or_post_id)
        post.likes += 1
        post.save()
        user_likes_post_instance = UserHasLikedPost.get_or_create(comment_or_post_id)
        user_likes_post_instance.save()
        new_likes = Post.get(comment_or_post_id).likes
    else:
        comment = Comment.get(comment_or_post_id)
        comment.likes += 1
        comment.save()
        user_likes_comment_instance = UserHasLikedComment.get_or_create(comment_or_post_id)
        user_likes_comment_instance.save()
        new_likes = Comment.get(comment_or_post_id).likes

    return HttpResponse(new_likes)

def get_view_post_context_dict(request, post_id):

    post = Post.objects.get(post_id=post_id)
    post_user = UserProfile.objects.get(user_id = post.user_id)
    comment = Comment.objects.filter(post_id = post_id).order_by('-date_posted').order_by('-time_posted')[0]
    current_user = request.user
    try:
        has_user_liked_post = UserHasLikedPost.get(user_id = current_user.user_id, post_id = post_id)
    except:
        has_user_liked_post = False
    else:
        has_user_liked_post = True
    try:
        has_user_liked_comment = UserHasLikedComment.get(user_id = current_user.user_id, post_id = post_id)
    except:
        has_user_liked_comment = False
    else:
        has_user_liked_comment = True
    context_dict = {'post': post, 'comment': comment, 'user': current_user, 'post_user': post_user,
                    'has_user_liked_post': has_user_liked_post,
                    'has_user_liked_comment': has_user_liked_comment}

    return context_dict
def view_individual_post(request, post_id):

    context_dict = get_view_post_context_dict(request, post_id)

    url = 'thepetproject/view_individual_post.html'
    return render(request, url , context = context_dict)

def create_comment(request):
    post_id = request.GET("post_id")
    post = Post.objects.get(post_id=post_id)
    comment_text = request.POST("comment_text")
    current_user = request.user
    context_dict = get_view_post_context_dict(request)

    url = 'thepetproject/posts/'+ post_id + 'create-comment'
    return render(request, url, context=context_dict)

def add_comment(request):
    post_id = request.GET("post_id")
    post = Post.objects.get(post_id=post_id)
    comment_text = request.POST("comment_text")
    current_user = request.user
    new_comment = Comment.get_or_create(user_id =current_user.user_id, post_id = post_id, text = comment_text)
    new_comment.save()
    url = 'thepetproject/posts/' + post_id
    context_dict = get_view_post_context_dict(request)
    return render(request, url, context=context_dict)

    post_list = Post.objects.order_by('-likes')[:3]
    context_dict = {}
    context_dict['posts'] = post_list
    return render(request, 'thepetproject/index.html', context=context_dict)

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

