# Generated by Django 5.1 on 2024-11-06 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_alter_activity_date_alter_activity_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attend',
            name='rep_decrease',
            field=models.BooleanField(default=False),
        ),
    ]
