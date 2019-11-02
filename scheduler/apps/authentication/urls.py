from django.urls import path
from django.conf.urls import url
from .views import CreateUserAPIView, LoginUser


urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', LoginUser.as_view())
]
