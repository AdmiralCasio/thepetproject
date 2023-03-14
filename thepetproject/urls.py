from django.urls import path
from thepetproject import views
from django.contrib.auth.views import LoginView

app_name = 'thepetproject'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/', views.profile_page, name='profile_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('my-account/', views.my_account, name='myaccount'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sign-up/', views.register, name='sign-up'),
    path('delete-account', views.delete_account, name='delete-account'),
]

