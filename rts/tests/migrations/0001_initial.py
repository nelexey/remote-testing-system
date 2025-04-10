# Generated by Django 5.1.4 on 2024-12-19 10:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('test', models.JSONField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=50)),
                ('duration', models.IntegerField(null=True)),
                ('attempts_allowed', models.IntegerField(default=1)),
                ('is_published', models.BooleanField(default=False)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tests',
            },
        ),
        migrations.CreateModel(
            name='TestStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField()),
                ('max_result', models.IntegerField()),
                ('time_spent', models.IntegerField(null=True)),
                ('date_taken', models.DateTimeField(default=django.utils.timezone.now)),
                ('passed', models.BooleanField()),
                ('attempt_number', models.IntegerField(default=1)),
                ('percentage', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'statistics',
            },
        ),
    ]
