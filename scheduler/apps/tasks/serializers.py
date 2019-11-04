from rest_framework import serializers
from .models import Task
from scheduler.apps.authentication.models import User


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
    assigned_to = serializers.StringRelatedField(many=True)

    def to_internal_value(self, value):
        # try:
        #     for user_id in value:
        #         user = User.objects.filter(pk=user_id).first()
        #         if not user:
        #             raise serializers.ValidationError(
        #                 'The assigned user does not exist.'
        #             )
        # except ValueError:
        #     raise serializers.ValidationError(
        #         'id must be an integer.'
        #     )
        try:
            return value
        except IntegrityError:
            raise serializers.ValidationError(
                'The assigned user does not exist.'
            )
        


    # def validate(self, data):
    #     username = data.get('assigned_to')
    #     if username:
    #         user = User.objects.filter(username=username).first()
    #         data['assigned_to'] = user.pk
            
    #         if not user:
    #             raise serializers.ValidationError(
    #                 'A user with this username does not exist.'
    #             )
    #     return data

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
