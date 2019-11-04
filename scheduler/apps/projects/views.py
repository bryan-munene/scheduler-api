from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer


def get_project(title):
    try:
        project = Project.objects.get(title=title)
        return project
    except Project.DoesNotExist:
        raise NotFound(
            {"error": "Project not found"}
        )


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Project.objects.order_by("created_at")
        serializer = ProjectSerializer(
            queryset, many=True, context={'request': request})
        return Response({"projects": serializer.data})

    def create(self, request):
        """create a project"""
        project = request.data
        project['created_by'] = request.user.id
        serializer = self.serializer_class(
            data=project, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Returns projects with the given title if exists"""
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project_data = request.data
        serializer = self.serializer_class(
            instance=project, data=project_data, partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response({"message": "project deleted successfully"}, status=status.HTTP_200_OK)