from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    
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

    def validate(self, data):
        title = data.get('title')
        project = Project.objects.filter(title=title).first()
        
        if project:
            raise serializers.ValidationError(
                'A project with this title and already exists.'
            )
        return data


    class Meta:
        model = Project
        fields = ('id',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'created_by')
