from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
import json
import base64

from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken

from .serializers import *
from .models import *

# Create your views here.


def serialize_user_info(user):
    return {
        'id':user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender
    }

class UserRegister(generics.GenericAPIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        try:
            request.data['email'] = request.data['email'].lower()
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = serializer.save()
            _, token = AuthToken.objects.create(user_obj)
            return Response({
                'user_info': serialize_user_info(user_obj),
                'token': token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print('UserRegister Error: ', str(e))
            return Response({'Invalid Request': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginApi(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self,request):
        try:
            request.data['username'] = request.data['username'].lower()
            usr = User.objects.get(username=request.data['username'])
        except Exception as e:
            return Response({"Invalid Credentials": "User email is not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if usr.is_active == False:
            return Response({"Account Error": "User Account Is Inactive.Contact Your Administrator"},status=status.HTTP_400_BAD_REQUEST)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _, token = AuthToken.objects.create(user)
        usr_info = {
            'id':user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender':user.gender
        }
        enc_str = json.dumps(usr_info)
        enc_usr_info = base64.b64encode(enc_str.encode('utf-8'))
        return Response({
            'info': enc_usr_info,
            'token':token
        })

class UserMinThrottle(UserRateThrottle):
    scope = 'user_min'

class SearchUser(generics.GenericAPIView):
    pagination_class = PageNumberPagination
    @swagger_auto_schema(request_body=SearchUserSerializer)
    def post(self, request):
        try:
            if '@' in request.data['req_data']:
                queryset = User.objects.filter(email__iexact=request.data['req_data'])
            else:
                queryset = User.objects.filter(
                    Q(first_name__icontains=request.data['req_data']) | Q(last_name__icontains=request.data['req_data'])
                    )
            page = self.paginate_queryset(queryset)
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            print('SearchUser Error: ', str(e))
            return Response({'Invalid Request': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class SendFriendRequest(generics.GenericAPIView):
    throttle_classes = [UserMinThrottle]
    @swagger_auto_schema(request_body=SendFriendRequestSerializer)
    def post(self, request):
        to_user_id = request.data['to_user_id']
        to_user = User.objects.get(id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if not created:
            return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)

class FriendRequestAction(generics.GenericAPIView):
    @swagger_auto_schema(request_body=FriendRequestActionSerializer)
    def post(self, request):
        serializer = FriendRequestActionSerializer(data=request.data)
        if serializer.is_valid():
            friend_request = FriendRequest.objects.get(id=serializer.validated_data['request_id'])
            if serializer.validated_data['action'] == 'accept':
                friend_request.status = 'accepted'
            elif serializer.validated_data['action'] == 'reject':
                friend_request.status = 'rejected'
            friend_request.save()
            return Response({'message': f'Friend request {friend_request.status}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            (Q(from_user=user.id) | Q(to_user=user.id)),
            status='accepted'
        )
        friend_ids = [fr.to_user.id if fr.from_user == user else fr.from_user.id for fr in friends]
        return User.objects.filter(id__in=friend_ids)

class ListPendingRequests(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user.id, status='pending')
