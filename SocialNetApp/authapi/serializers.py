from rest_framework import serializers
from rest_framework import validators
from datetime import datetime, date, timezone


from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'password', 'gender'
        )
        extra_kwargs = {
            'password':{'write_only':True},
            'email': {
                'required':True,
                'allow_blank':False,
                'validators':[
                    validators.UniqueValidator(
                        User.objects.all(), 'A user already registered with given email!'
                    )
                ]
            }
        }

    def create(self, validated_data):
        print(validated_data, 'validated_data')
        user_obj = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['email'],
            gender = validated_data['gender'],
            is_active = validated_data['is_active'],
            date_joined = datetime.now(timezone.utc),
            created = datetime.now(timezone.utc)
        )
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return user_obj

class SearchUserSerializer(serializers.Serializer):
    req_data = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'id')

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class SendFriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

class FriendRequestActionSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])
