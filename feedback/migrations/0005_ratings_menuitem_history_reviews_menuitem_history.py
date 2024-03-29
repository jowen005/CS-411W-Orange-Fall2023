# Generated by Django 4.2.4 on 2023-10-21 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0002_menuitemhistory_delete_mealhistory'),
        ('feedback', '0004_remove_ratings_meal_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='menuItem_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patron.menuitemhistory'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='menuItem_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patron.menuitemhistory'),
        ),
    ]
