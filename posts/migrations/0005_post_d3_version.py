# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20171002_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='D3_version',
            field=models.CharField(choices=[('v3', "{% static 'simplesocial/js/d3_v3.min.js' %}"), ('v4', "{% static 'simplesocial/js/d3_v4.min.js' %}")], default=' ', max_length=250),
        ),
    ]
