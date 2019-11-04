from django.db import models
from scheduler.apps.authentication.models import User

class Project(models.Model):
    """Create models for the articles"""
    title = models.CharField(max_length=500, blank=False, unique=True)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """create a project and save to the database"""
        super().save(*args, **kwargs)
