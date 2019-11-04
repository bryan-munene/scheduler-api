from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=30,
        min_length=8,
        write_only=True
    )

    def validate_username(self, data):
        if re.match(r'^[0-9]+[A-Za-z0-9]*$', data):
            raise serializers.ValidationError(
                "Username cannot contain numbers or special characters only")
        return data

    def validate_password(self, data):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).*',
                        data):
            raise serializers.ValidationError(
                "Password must contain a number, capital letter and special charachter")  # noqa
        return data

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username',
                    'date_joined', 'password', 'updated_at')
        

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        
        return {
            'email': user.email,
            'token': user.token
        }
