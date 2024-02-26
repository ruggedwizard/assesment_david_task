from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Task


"""TASK SERIALIZER, WITH CUSTOM ERROR MESSAGE FOR INVALID STATUS INPUT FIELD"""
class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = ['id','title','description','completed','status', 'created_by']
        extra_kwargs = {
            'status':{
                'error_messages':{
                    'invalid_choice':'Invalid Status, Available Options are: todo,in progress and completed'
                }
            }
        }

""" USER REGISTERATION SERIALIZER"""
class RegisterSerializer(serializers.ModelSerializer):
    # Set minimum length constraint for user when crearing an account
    password = serializers.CharField(max_length=68,min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['username','password']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
