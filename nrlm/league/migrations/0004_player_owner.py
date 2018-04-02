# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-02 17:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0003_auto_20180402_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to=settings.AUTH_USER_MODEL),
        ),
    ]