from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('follow/<str:username>/', views.toggle_follow_view, name='toggle_follow'),
    path('<str:username>/followers/', views.followers_view, name='followers'),
    path('<str:username>/following/', views.following_view, name='following'),
    path('<str:username>/', views.user_page_view, name='user_page'),
]
