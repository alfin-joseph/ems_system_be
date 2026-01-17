from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, EmployeeFieldDefinition, EmployeeForm


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, min_length=8, required=True)
    new_password2 = serializers.CharField(write_only=True, min_length=8, required=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})
        return value


class EmployeeFieldDefinitionSerializer(serializers.ModelSerializer):
    """Serializer for employee field definitions"""
    class Meta:
        model = EmployeeFieldDefinition
        fields = [
            'id', 'field_name', 'field_label', 'field_type', 'is_required',
            'order', 'options', 'min_length', 'max_length', 'min_value',
            'max_value', 'pattern', 'default_value', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee with fixed and dynamic fields"""
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'name', 'email', 'department', 'role',
            'dynamic_data', 'status', 'hire_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing employees"""
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'status', 'hire_date']


class EmployeeFormSerializer(serializers.ModelSerializer):
    """Serializer for employee custom forms"""
    all_fields = serializers.SerializerMethodField()
    
    class Meta:
        from .models import EmployeeForm
        model = EmployeeForm
        fields = ['id', 'form_name', 'form_description', 'fields', 'all_fields', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_all_fields(self, obj):
        """Return all fields (fixed + custom) sorted by order"""
        return obj.get_all_fields()
