from rest_framework import serializers
from scheduler.apps.tasks.models import Task
from scheduler.apps.authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'description',
                  'project',
                  'created_at',
                  'updated_at',
                  'assigned_to',
                  'is_complete',
                  'created_by')
