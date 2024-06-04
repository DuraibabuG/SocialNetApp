from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
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
        'last_name': user.last_namae,
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
            _, token = AuthToken.objects.create(user)
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
