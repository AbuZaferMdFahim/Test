from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
#from user.models import Manager

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username
class Manager(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    img = models.ImageField(upload_to='manager_images/')
    team = models.OneToOneField('Team', on_delete=models.SET_NULL, blank=True, null=True, related_name='team_manager')
    NID_number = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, null=True)
    ROLE_CHOICES = [
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager', editable=False)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    established = models.DateField()
    manager = models.OneToOneField(Manager, related_name='created_teams', on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.team_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.manager:
            manager = self.manager
            manager.team = self
            manager.save()

# Slot model
class Slot(models.Model):
    turf_name = models.CharField(max_length=100, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    team_name_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='slot_team_1',blank=True,null=True)
    team_name_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='slot_team_2',blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['turf_name', 'time'], name='unique_turf_time')
        ]

    def clean(self):
        if self.team_name_1 == self.team_name_2:
            raise ValidationError("Team_name_1 and Team_name_2 cannot be the same.")

    def __str__(self):
        return f"{self.turf_name} - {self.time}"

    #     for player in self.players.all():
    #         player.team = self
    #         player.save()

# class Player(models.Model):
#     GOALKEEPER = 'goalkeeper'
#     DEFENDER = 'defender'
#     MIDFIELDER = 'midfielder'
#     FORWARD = 'forward'

#     POSITION_CHOICES = [
#         (GOALKEEPER, 'Goalkeeper'),
#         (DEFENDER, 'Defender'),
#         (MIDFIELDER, 'Midfielder'),
#         (FORWARD, 'Forward'),
#     ]
    
#     RATING_CHOICES = [
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#         (6, '6'),
#         (7, '7'),
#         (8, '8'),
#         (9, '9'),
#         (10, '10'),
#     ]

#     unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     player_name = models.CharField(max_length=100)
#     img = models.ImageField(upload_to='player_images/')
#     bio = models.TextField(null=True)
#     kit = models.IntegerField(null=True,blank=True)
#     age = models.IntegerField()
#     position = models.CharField(
#         max_length=50,
#         choices=POSITION_CHOICES,
#         default=MIDFIELDER,
#     )
#     team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True, related_name='team_players')
#     NID_number = models.CharField(max_length=100)
#     nationality = models.CharField(max_length=100, null=True)
#     rating = models.IntegerField(choices=RATING_CHOICES,default=5)
#     ROLE_CHOICES = [
#         ('player', 'Player'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager', editable=False)
    
#     def __str__(self):
#         return self.player_name

