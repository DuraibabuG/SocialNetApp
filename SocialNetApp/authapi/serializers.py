from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from datetime import datetime, date, timezone


from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'password'
        )
        extra_kwargs = {
            'email': {
                'validators': [
                        UniqueValidator(
                            queryset=User.objects.all(),
                            message='Email already exisit!'
                        )
                    ]
            }
        }

    def create(self, validated_data):
        print(validated_data, 'validated_data')
        user_obj = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_namae'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            date_joined=datetime.now(timezone.utc),
            created=datetime.now(timezone.utc)
        )
        user_obj.set_password(validated_data['password'])
        return user_obj
