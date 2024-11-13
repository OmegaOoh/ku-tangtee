# Generated by Django 5.1.1 on 2024-11-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_rename_minium_reputation_score_activity_minimum_reputation_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]