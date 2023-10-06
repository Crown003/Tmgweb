# Generated by Django 4.2.4 on 2023-09-26 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('teamname', models.CharField(max_length=40, unique=True, verbose_name='Team Name')),
                ('teamBio', models.TextField(max_length=250, verbose_name='Bio')),
                ('game', models.CharField(max_length=50, verbose_name='game')),
                ('numberOfPlayers', models.IntegerField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('manager', 'Team Manager'), ('player', 'Player'), ('guest', 'Guest')], max_length=20)),
                ('selected_games', models.ManyToManyField(to='main.game')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerOne', models.CharField(blank=True, max_length=60, unique=True, verbose_name='IGN Player 1')),
                ('playerOneEmail', models.EmailField(max_length=254)),
                ('playerOneIGID', models.IntegerField(blank=True, unique=True, verbose_name='PLAYER 1 In-game ID:')),
                ('playerTwo', models.CharField(blank=True, max_length=60, unique=True, verbose_name='IGN Player 2')),
                ('playerTwoEmail', models.EmailField(max_length=254)),
                ('playerTwoIGID', models.IntegerField(blank=True, unique=True, verbose_name='PLAYER 2 In-game ID:')),
                ('playerThree', models.CharField(blank=True, max_length=60, unique=True, verbose_name='IGN Player 3')),
                ('playerThreeEmail', models.EmailField(max_length=254)),
                ('playerThreeIGID', models.IntegerField(blank=True, unique=True, verbose_name='PLAYER 3 In-game ID:')),
                ('playerFour', models.CharField(blank=True, max_length=60, unique=True, verbose_name='IGN Player 4')),
                ('playerFourEmail', models.EmailField(max_length=254)),
                ('playerFourIGID', models.IntegerField(blank=True, unique=True, verbose_name='PLAYER 4 In-game ID:')),
                ('playerFive', models.CharField(blank=True, max_length=60, unique=True, verbose_name='IGN Player 5')),
                ('playerFiveEmail', models.EmailField(max_length=254)),
                ('playerFiveIGID', models.IntegerField(blank=True, unique=True, verbose_name='PLAYER 5 In-game ID:')),
                ('team', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.team')),
            ],
        ),
    ]
