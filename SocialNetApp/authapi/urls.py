from django.urls import path
from authapi import views
from knox import views as knox_views

urlpatterns = [
    path('sign_up/', views.UserRegister.as_view()),
    path('login/', views.LoginApi.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('search_user/', views.SearchUser.as_view()),
    path('friend_request_send/', views.SendFriendRequest.as_view()),
    path('frien_request_action/', views.FriendRequestAction.as_view()),
    path('friends_list/', views.ListFriendsView.as_view()),
    path('friend_requests_pending/', views.ListPendingRequests.as_view()),
]