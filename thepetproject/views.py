from django.shortcuts import render
from django.http import HttpResponse
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedPost, UserHasLikedComment
def index(request):
    return render(request, 'thepetproject/index.html')

def view_individual_post(request, post_id):

    post = Post.objects.get(post_id)
    comment = Comment.objects.order_by('-date').order_by('-time')[0]
    current_user = request.user
    context_dict = {'post': post, 'comment': comment, 'user': current_user}

    return render(request, 'thepetproject/view_individual_post.html', context_dict)

