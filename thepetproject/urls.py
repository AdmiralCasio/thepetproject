from django.urls import path
from thepetproject import views


urlpatterns = [
    path('', views.index, name='index'),
]

