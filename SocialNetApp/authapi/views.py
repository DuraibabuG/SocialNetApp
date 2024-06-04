from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework import permissions
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
import json
import base64

from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken

from .serializers import *
from .models import *

# Create your views here.

class UserSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

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
            # request.data['email'] = request.data['email'].lower()
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

class SearchUser(generics.GenericAPIView):
    pagination_class = [UserSetPagination]
    @swagger_auto_schema(request_body=SearchUserSerializer)
    def post(self, request):
        try:
            print(request.data['req_data'], 'input_data')
            # user_list = User.objects.filter(email__contains=request.data['req_data']
            #     ).values('first_name', 'last_name', 'email', 'id')
            # return Response(user_list, status=status.HTTP_200_OK)
            query = self.request.query_params.get('q', None)
            if query:
                queryset = queryset.filter(username__icontains=query) | queryset.filter(email__icontains=query)
            return queryset
        except Exception as e:
            print('SearchUser Error: ', str(e))
            return Response({'Invalid Request': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendFriendRequest(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class AcceptFriendRequest(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'accepted'
        instance.save()
        return Response({'status': 'Friend request accepted'}, status=status.HTTP_200_OK)

class RejectFriendRequest(generics.DestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]