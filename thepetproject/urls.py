from django.urls import path
from thepetproject import views

app_name = 'thepetproject'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<slug:post_id>', views.view_individual_post, name='view_individual_post'),
    path('like/', views.like, name='like'),
    path('posts/<slug:post_id>/create-comment', views.create_comment, name='create_comment'),
    path('posts/slug:post_id>/add-comment', views.add_comment, name='add_comment'),
    path('profile/<slug:username>/', views.profile_page, name='profile_page'),
]

