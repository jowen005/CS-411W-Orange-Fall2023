# Generated by Django 4.2.4 on 2023-10-21 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_ratings_meal_history_reviews_meal_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratings',
            name='meal_history',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='meal_history',
        ),
    ]