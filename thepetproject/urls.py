from django.urls import path
from thepetproject import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/', views.profile_page, name='profile_page'),
]

