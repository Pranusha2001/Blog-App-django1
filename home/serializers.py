from rest_framework import serializers
from .models import BlogPost
from .models import UserProfile
from .models import Comment
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify
from Blog.config import ROLE_CHOICES
from django.utils.text import slugify
from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'role', 'author']
        read_only_fields = ['id', 'slug', 'author']

        
    def clean_title(self):
        title = self.validated_data['title']
        slug = slugify(title)
        if BlogPost.objects.filter(slug=slug).exists():
            raise serializers.ValidationError('A blog post with this title already exists.')
        return slug

    def create(self, validated_data):
        validated_data['slug'] = self.clean_title()
        return super().create(validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = UserProfile
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'       


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    
User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        # Validate the password against Django's built-in password validators
        validate_password(value)
        return value

    def validate(self, data):
        # Ensure the password and confirm_password fields match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        # Ensure the username and email are unique
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already taken")
        return data

    def create(self, validated_data):
        # Create the new user
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            
        )
        return user    