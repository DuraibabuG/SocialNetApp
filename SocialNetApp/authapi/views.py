from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.authentication import BasicAuthentication


from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from .models import *

# Create your views here.

class UserRegister(generics.GenericAPIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = serializer.save()
            out_data = {}
            if user_obj:
                out_data['first_name'] = user_obj.first_name
                out_data['last_name'] = user_obj.last_name
                out_data['email'] = user_obj.email
                out_data['is_active'] = user_obj.is_active
            else:
                raise Exception('User regiter error!')
            return Response(out_data, status=status.HTTP_200_OK)
        except Exception as e:
            print('UserRegister Error: ', str(e))
            return Response({'Invalid Request': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Login(generics.GenericAPIView):
    # @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        pass