from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('lists/new/', views.create_list_view, name='create_list'),
]
