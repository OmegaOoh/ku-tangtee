# Generated by Django 5.1.1 on 2024-11-09 06:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_merge_20241109_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='minium_reputation_score',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
