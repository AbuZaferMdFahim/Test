# Generated by Django 4.2.4 on 2024-07-16 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_slot_slot_unique_turf_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='team_name_1',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='team_name_2',
        ),
    ]
