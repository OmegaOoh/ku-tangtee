# Generated by Django 5.1.1 on 2024-10-30 02:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(blank=True, max_length=30, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('is_single', models.BooleanField(blank=True, null=True)),
                ('student_id', models.IntegerField(blank=True, null=True)),
                ('generation', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('faculty', models.CharField(max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('tel', models.CharField(blank=True, max_length=10, null=True)),
                ('contact', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
