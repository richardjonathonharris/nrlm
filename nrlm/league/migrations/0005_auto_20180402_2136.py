# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-02 21:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0004_player_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='round_num',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]