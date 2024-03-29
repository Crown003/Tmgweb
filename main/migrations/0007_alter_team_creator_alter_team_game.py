# Generated by Django 4.2.4 on 2023-09-29 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_alter_team_creator_alter_team_teamname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='game',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.game'),
        ),
    ]
