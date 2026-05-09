from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('lists/new/', views.create_list_view, name='create_list'),
    path('lists/<int:pk>/like/', views.toggle_like_view, name='toggle_like'),
    path('lists/<int:pk>/comment/', views.add_comment_view, name='add_comment'),
]
