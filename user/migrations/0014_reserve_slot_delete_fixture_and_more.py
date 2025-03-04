# Generated by Django 4.2.4 on 2024-07-16 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_fixture_team_name_1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve_slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_at', models.DateTimeField(auto_now_add=True)),
                ('chosen_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.manager')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.slot')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.team')),
            ],
        ),
        migrations.DeleteModel(
            name='Fixture',
        ),
        migrations.AddConstraint(
            model_name='reserve_slot',
            constraint=models.UniqueConstraint(fields=('team', 'slot'), name='unique_team_slot'),
        ),
    ]
