from django.shortcuts import render
from django.http import HttpResponse
from thepetproject.models import Post

def index(request):
    post_list = Post.objects.order_by('-likes')[:3]
    context_dict = {}
    context_dict['posts'] = post_list
    return render(request, 'thepetproject/index.html', context=context_dict)

