from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


def get_task(title):
    try:
        task = Task.objects.get(title=title)
        return task
    except Task.DoesNotExist:
        raise NotFound(
            {"error": "Task not found"}
        )


class TaskViewSet(viewsets.ViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk):
        queryset = Task.objects.filter(project=pk)
        serializer = TaskSerializer(
            queryset, many=True, context={'request': request})
        return Response({"projects tasks": serializer.data})

    def create(self, request, pk):
        """create a task"""
        task = request.data
        task['created_by'] = request.user.id
        task['project'] = pk
        serializer = self.serializer_class(
            data=task, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk, id=None):
        """Returns projects with the given title if exists"""
        queryset = Task.objects.filter(project=pk)
        task = get_object_or_404(queryset, pk=id)
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk, id=None):
        queryset = Task.objects.filter(project=pk)
        task = get_object_or_404(queryset, pk=id)
        task_data = request.data
        serializer = self.serializer_class(
            instance=task, data=task_data, partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, id=None):
        queryset = Task.objects.filter(project=pk)
        task = get_object_or_404(queryset, pk=id)
        task.delete()
        return Response({"message": "task deleted successfully"}, status=status.HTTP_200_OK)