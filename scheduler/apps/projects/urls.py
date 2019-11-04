from django.urls import path, include
from django.conf.urls import url
from scheduler.apps.projects import views 

app_name = "projects"

urlpatterns = [path('projects/', views.ProjectViewSet.as_view(
    {'get': 'list', "post": "create"}), name='projects-all'),
    path('projects/<pk>/', views.ProjectViewSet.as_view(
        {"get": "retrieve", "patch": "partial_update",
         "delete": "destroy"}), name='single-project'), 
    path('projects/<pk>/', include('scheduler.apps.tasks.urls',
                                             namespace='tasks')),
    ]
