from django.urls import path
from authapi import views

urlpatterns = [
    path('user_register/', views.UserRegister.as_view()),
    path('login/', views.Login.as_view()),
]