from django.urls import path
from thepetproject import views

app_name = 'thepetproject'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/', views.profile_page, name='profile_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('upload_post/', views.upload_post_page, name='upload_post_page')
]

