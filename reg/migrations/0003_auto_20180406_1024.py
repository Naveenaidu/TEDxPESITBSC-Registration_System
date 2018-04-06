# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0002_auto_20151001_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='college',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='github_url',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='linkedin_url',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='noc_submitted',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='recharge_possible',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='service_provider',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='team',
        ),
        migrations.AddField(
            model_name='participant',
            name='reg_type',
            field=models.CharField(default=b'Student', max_length=15),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
