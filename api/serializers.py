from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile,Team
from rest_framework.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'mobile', 'dob', 'avatar']
        extra_kwargs = {
            'avatar': {'required': False, 'allow_null': True},
        }

# api/serializers.py

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['user']

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):  # Remove password_confirm from validated data
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )

        # Check if profile exists for user
        if Profile.objects.filter(user=user).exists():
            raise ValidationError("Profile already exists for this user.")

        # Create profile for user
        avatar_data = profile_data.pop('avatar', None)
        profile = Profile.objects.create(
            user=user,
            avatar=avatar_data,
            **profile_data
        )

        print(f"User created: {user.username}")  # Debug statement
        print(f"Profile created: {profile.name}")  # Debug statement

        return user
    

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'team_name', 'logo', 'established', 'created_by']
