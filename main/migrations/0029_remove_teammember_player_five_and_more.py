# Generated by Django 4.2.4 on 2023-11-26 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0028_alter_team_members_alter_teammember_player_five_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='player_five',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='player_four',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='player_one',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='player_six',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='player_three',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='player_two',
        ),
        migrations.AddField(
            model_name='teammember',
            name='players',
            field=models.ManyToManyField(blank=True, related_name='team_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team', to='main.teammember'),
        ),
    ]