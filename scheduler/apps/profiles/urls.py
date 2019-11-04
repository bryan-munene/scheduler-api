from django.urls import path, include
from django.conf.urls import url
from scheduler.apps.profiles import views 

app_name = "tasks"

urlpatterns = [path('tasks/<id>/', views.ProfileUserViewSet.as_view(
    {'get': 'list'}), name='user-all-tasks'),
    path('projects/<pk>/tasks/<id>/', views.ProfileUserProjectViewSet.as_view(
        {"get": "list"}), name='user-project-task'),
    ]
