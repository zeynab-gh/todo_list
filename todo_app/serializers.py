from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo, Category
# در فایل serializers.py اضافه کنید
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'icon', 'todo_count', 'user']
    
    def get_todo_count(self, obj):
        return obj.todos.count()
    
    def create(self, validated_data):
        """اتوماتیک کاربر جاری را به عنوان مالک تنظیم می‌کند"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TodoSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    days_until_due = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'is_completed', 
            'category', 'category_name', 'priority', 'due_date',
            'created_at', 'updated_at', 'user', 'days_until_due'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_days_until_due(self, obj):
        return obj.days_until_due()
    
    def create(self, validated_data):
        """اتوماتیک کاربر جاری را به عنوان مالک تنظیم می‌کند"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'category', 'priority', 'due_date']



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
            
        attrs['user'] = user
        return attrs