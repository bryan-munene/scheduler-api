from django.urls import path, include
from django.conf.urls import url
from scheduler.apps.tasks import views 

app_name = "tasks"

urlpatterns = [path('tasks/', views.TaskViewSet.as_view(
    {'get': 'list', "post": "create"}), name='tasks-all'),
    path('tasks/<id>/', views.TaskViewSet.as_view(
        {"get": "retrieve", "patch": "partial_update",
         "delete": "destroy"}), name='single-task'),
    ]
