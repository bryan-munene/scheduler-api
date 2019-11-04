from django.db import models
from scheduler.apps.authentication.models import User
from scheduler.apps.projects.models import Project


class Task(models.Model):
    """
    Creates model for Comments
    """

    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=False, max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT)
    assigned_to = models.CharField(null=True, max_length=20)  
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title