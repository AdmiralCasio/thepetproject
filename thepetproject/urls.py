from django.urls import path
from thepetproject import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.view_individual_post, name='view_individual_post'),
    path('like/', views.like, name='like'),
    path('create-comment', views.create_comment, name='create_comment')
]

