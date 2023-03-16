from django.urls import path
from thepetproject import views
from django.contrib.auth.views import LoginView

app_name = 'thepetproject'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<slug:post_id>', views.view_individual_post, name='view_individual_post'),
    path('posts/<slug:post_id>/like', views.like_post, name='like_post'),
    path('posts/<slug:post_id>/<slug:comment_id>/like', views.like_comment, name='like_comment'),
    path('posts/<slug:post_id>/create-comment', views.create_comment, name='create_comment'),
    path('profile/<slug:username>/', views.profile_page, name='profile_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('my-account/', views.my_account, name='myaccount'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sign-up/', views.register, name='sign-up'),
]

