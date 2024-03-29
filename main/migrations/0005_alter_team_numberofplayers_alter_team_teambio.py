# Generated by Django 4.2.4 on 2023-09-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userprofile_bgmi_id_userprofile_bgmi_ign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='numberOfPlayers',
            field=models.IntegerField(choices=[(4, '4 players'), (5, '5 players'), (6, '6 players')]),
        ),
        migrations.AlterField(
            model_name='team',
            name='teamBio',
            field=models.TextField(max_length=250, verbose_name='Description'),
        ),
    ]
