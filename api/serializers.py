from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile,Team,Manager,Slot,Reserve_slot,Fixture
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
    
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'
        extra_kwargs = {
            'img': {'required': False, 'allow_null': True},
        }
        read_only_fields = ['user', 'unique_id', 'role']

class TeamSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(write_only=True)

    class Meta:
        model = Team
        fields = ['team_name', 'logo', 'established', 'manager_name']
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        manager_name = validated_data.pop('manager_name')
        try:
            manager = Manager.objects.get(name=manager_name)
        except Manager.DoesNotExist:
            raise serializers.ValidationError("Manager with this name does not exist")
        
        team = Team.objects.create(manager=manager, **validated_data)
        manager.team = team
        manager.save()
        return team

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'
        
class ReserveSlotSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    manager_name = serializers.CharField(source='manager_name.name', read_only=True)
    turf_name = serializers.CharField(source='slot.turf_name', read_only=True)
    date = serializers.DateField(source='slot.date', read_only=True)
    time = serializers.TimeField(source='slot.time', read_only=True)
    location = serializers.CharField(source='slot.location', read_only=True)
    address = serializers.CharField(source='slot.address', read_only=True)

    class Meta:
        model = Reserve_slot
        fields = ['team_name', 'turf_name', 'date', 'time', 'location', 'address', 'manager_name', ]

    def create(self, validated_data):
        # Assuming 'team' and 'slot' are required fields in the serializer
        validated_data['team'] = self.context['request'].user.manager.team
        validated_data['manager_name'] = self.context['request'].user.manager
        reserve_slot = Reserve_slot.objects.create(**validated_data)
        return reserve_slot
        
class FixtureSerializer(serializers.ModelSerializer):
    team_1_name = serializers.CharField(source='team_1.team_name', read_only=True)
    team_2_name = serializers.CharField(source='team_2.team_name', read_only=True)
    turf_name = serializers.CharField(source='slot.turf_name', read_only=True)
    date = serializers.DateField(source='slot.date', read_only=True)
    time = serializers.TimeField(source='slot.time', read_only=True)
    location = serializers.CharField(source='slot.location', read_only=True)
    address = serializers.CharField(source='slot.address', read_only=True)

    class Meta:
        model = Fixture
        fields = ['team_1_name','team_2_name', 'turf_name', 'date', 'time', 'location', 'address']     
        
# class FixtureSerializer(serializers.ModelSerializer):
#     slot_location = serializers.CharField(source='slot.location')
#     slot_time = serializers.TimeField(source='slot.time')
#     slot_area = serializers.CharField(source='slot.address')
#     slot_turf_name = serializers.CharField(source='slot.turf_name')

#     class Meta:
#         model = Fixture
#         fields = ['id', 'team_name_1', 'team_name_2', 'slot_location', 'slot_time', 'slot_area', 'slot_turf_name']
  
    
# class SlotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slot
#         fields = ['id', 'turf_name', 'time', 'location', 'address', 'team_name_1', 'team_name_2']
#         extra_kwargs = {
#             'team_name_1': {'required': False, 'allow_null': True},
#             'team_name_2': {'required': False, 'allow_null': True},
#         }