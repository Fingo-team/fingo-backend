# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 07:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0006_merge_20161206_2105'),
        ('movie', '0002_auto_20161209_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(default=0.0)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='UserDirector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(default=0.0)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Director')),
            ],
        ),
        migrations.CreateModel(
            name='UserGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(default=0.0)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='UserNation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(default=0.0)),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Nation')),
            ],
        ),
        migrations.CreateModel(
            name='UserStatistics',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='member.FingoUser')),
                ('movie_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserScores',
            fields=[
                ('user_statistics', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_statistics.UserStatistics')),
                ('point_five', models.IntegerField(default=0)),
                ('one', models.IntegerField(default=0)),
                ('one_point_five', models.IntegerField(default=0)),
                ('two', models.IntegerField(default=0)),
                ('two_point_five', models.IntegerField(default=0)),
                ('three', models.IntegerField(default=0)),
                ('three_point_five', models.IntegerField(default=0)),
                ('four', models.IntegerField(default=0)),
                ('four_point_five', models.IntegerField(default=0)),
                ('five', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='usernation',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_statistics.UserStatistics'),
        ),
        migrations.AddField(
            model_name='usergenre',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_statistics.UserStatistics'),
        ),
        migrations.AddField(
            model_name='userdirector',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_statistics.UserStatistics'),
        ),
        migrations.AddField(
            model_name='useractor',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_statistics.UserStatistics'),
        ),
    ]
