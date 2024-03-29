# Generated by Django 4.2.4 on 2023-10-17 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0001_initial'),
        ('feedback', '0002_remove_reviews_restaurant_replies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='meal_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patron.mealhistory'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='meal_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patron.mealhistory'),
        ),
    ]
