# Generated by Django 4.2.4 on 2023-11-11 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_teammembers_remove_team_members_team_members'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamMembers',
            new_name='TeamMember',
        ),
    ]