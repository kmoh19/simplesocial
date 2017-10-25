# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_d3_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='js_file_1',
            field=models.FileField(blank=True, upload_to=posts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='post',
            name='js_file_2',
            field=models.FileField(blank=True, upload_to=posts.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='D3_version',
            field=models.CharField(blank=True, choices=[('/static/simplesocial/js/d3_v3.min.js', 'v3'), ('/static/simplesocial/js/d3_v4.min.js', 'v4')], default=' ', max_length=250),
        ),
    ]
