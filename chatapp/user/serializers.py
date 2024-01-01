from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import User


class UserList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'email']


# class MessageSerializer(serializers.Serializer):
#     message = serializers.CharField()
#     sender = serializers.IntegerField()

class AuthSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials',)
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
