# Generated by Django 4.2.4 on 2023-11-23 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appsatisfactionanalytics',
            name='number_of_rating_since',
        ),
    ]