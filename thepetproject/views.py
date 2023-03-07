from django.shortcuts import render
from django.http import HttpResponse
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedPost, UserHasLikedComment
def index(request):
    return render(request, 'thepetproject/index.html')

def view_individual_post(request, post_id):

    post = Post.objects.get(post_id)
    comment = Comment.objects.order_by('-date').order_by('-time')[0]
    current_user = request.user
    try:
        has_user_liked_post = UserHasLikedPost.get(current_user.username)
    except:
        has_user_liked_post = False
    else:
        has_user_liked_post = True
    try:
        has_user_liked_comment = UserHasLikedComment.get(current_user.username)
    except:
        has_user_liked_comment = False
    else:
        has_user_liked_comment = True
    context_dict = {'post': post, 'comment': comment, 'user': current_user,
                    'has_user_liked_post': has_user_liked_post,
                    'has_user_liked_comment': has_user_liked_comment}

    return render(request, 'thepetproject/view_individual_post.html', context_dict)

