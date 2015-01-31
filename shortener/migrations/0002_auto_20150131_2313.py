# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlpair',
            name='original_url',
            field=models.URLField(max_length=1000),
            preserve_default=True,
        ),
    ]
