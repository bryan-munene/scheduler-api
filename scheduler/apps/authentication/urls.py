from django.urls import path
from django.conf.urls import url
from .views import CreateUserAPIView, LoginUser

app_name = "authentication"

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', LoginUser.as_view())
]
