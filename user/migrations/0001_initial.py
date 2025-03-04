# Generated by Django 4.2.4 on 2024-07-12 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bio', models.TextField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('img', models.ImageField(upload_to='manager_images/')),
                ('NID_number', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(choices=[('manager', 'Manager')], default='manager', editable=False, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('player_name', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='player_images/')),
                ('bio', models.TextField(null=True)),
                ('kit', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField()),
                ('position', models.CharField(max_length=50)),
                ('NID_number', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100, null=True)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=5)),
                ('role', models.CharField(choices=[('player', 'Player')], default='manager', editable=False, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='club_logos/')),
                ('established', models.DateField()),
                ('manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_team', to='user.manager')),
                ('players', models.ManyToManyField(blank=True, related_name='teams', to='user.player')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('dob', models.DateField()),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_players', to='user.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
