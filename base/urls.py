from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('update-user/', views.update_user, name='update-user'),
    path('topics/', views.topics_page, name='topics'),
    path('activities/', views.activities_page, name='activities'),
]
