from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from scheduler.apps.tasks.models import Task
from .serializers import ProfileSerializer


def get_task(title):
    try:
        task = Task.objects.get(title=title)
        return task
    except Task.DoesNotExist:
        raise NotFound(
            {"error": "Task not found"}
        )


class ProfileUserViewSet(viewsets.ViewSet):
    queryset = Task.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, id):
        queryset = Task.objects.filter(assigned_to=id)
        serializer = ProfileSerializer(
            queryset, many=True, context={'request': request})
        return Response({"User all tasks": serializer.data})

class ProfileUserProjectViewSet(viewsets.ViewSet):
    queryset = Task.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk, id):
        queryset = Task.objects.filter(project=pk, assigned_to=id)
        serializer = ProfileSerializer(
            queryset, many=True, context={'request': request})
        return Response({"User Project tasks": serializer.data})
