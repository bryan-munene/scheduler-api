
from __future__ import unicode_literals
from django.db import models
from django.db import transaction
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.conf import settings
from datetime import datetime as date_time, timedelta
import jwt


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """
    implements a fully featured User Model woth admin compliant permissions
    """

    email = models.EmailField(unique=True, db_index=True, null=False)
    username = models.CharField(max_length=30, blank=True, null=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        This method allows us to get the token by calling 'user.token'
        """
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        """This method generates a JSON Web Token during user signup"""
        user_details = {'email': self.email,
                        'username': self.username}
        token = jwt.encode(
            {
                'user_data': user_details,
                'exp': date_time.now() + timedelta(days=7)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token.decode('utf-8')
