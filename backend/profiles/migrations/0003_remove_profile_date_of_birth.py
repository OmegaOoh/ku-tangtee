# Generated by Django 5.1.1 on 2024-11-01 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_generation_profile_ku_generation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_of_birth',
        ),
    ]