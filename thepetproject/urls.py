from django.urls import path
from thepetproject import views


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.view_individual_post, name='view_individual_post'),
    path('', views.like, name='like')
]

