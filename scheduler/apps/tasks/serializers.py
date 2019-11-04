from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    
    title = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            'required': 'title cannot be empty',
            'max_length': 'title cannot exceed 500 characters'
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'the description cannot be empty'
        }
    )

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
