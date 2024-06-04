from django.urls import path
from authapi import views
from knox import views as knox_views

urlpatterns = [
    path('user_register/', views.UserRegister.as_view()),
    path('login/', views.LoginApi.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]