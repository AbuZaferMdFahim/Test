# Generated by Django 4.2.4 on 2024-07-12 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_player_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_manager', to='user.team'),
        ),
    ]
