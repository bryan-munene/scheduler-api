import jwt
# import simplejson as json
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status
from django.http import HttpResponse
from .serializers import UserSerializer
from .models import User
# Create your views here.


class CreateUserAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {
                    'Error': "Please provide a email and a password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response(
                {
                    "Error": "Invalid email or password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            payload = {
                'email': user.email,
                'password': user.password
            }
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

            response_details = {
                'token': jwt_token,
                'message': "You have successfully logged in",
                'status': status.HTTP_200_OK
            }
            return Response(response_details, status=response_details['status'])
        else:
            return Response(
                    {"Error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )


class TokenAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower != b'token':
            return None

        if len(auth) == 1:
            message = 'Invalid token header. No credentials provided'
            raise exceptions.AuthenticationFailed(message)
        elif len(auth) > 2:
            message = 'Invalid token header'
            raise exceptions.AuthenticationFailed(message)

        try:
            token = auth[1]
            if token == "null":
                message = "Null token is not allowed"
                raise exceptions.AuthenticationFailed(message)

        except UnicodeError:
            message = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(message)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()
        payload = jwt.decode(token, "SECRET_KEY")
        email = payload['email']
        password = payload['password']
        msg = {'Error': 'Token mismatch', status: status.HTTP_401_UNAUTHORIZED}

        try:
            user = User.objects.get(
                email=email,
                password=password,
                is_active=True
            )

            if not user.token['token'] == token:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return HttpResponse({"Error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'
