# Generated by Django 4.2.4 on 2023-09-27 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_restaurant_sun_close'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Allergy_tag',
            new_name='AllergyTag',
        ),
        migrations.RenameModel(
            old_name='IngredientsTag',
            new_name='IngredientTag',
        ),
        migrations.RenameModel(
            old_name='Restriction_tag',
            new_name='RestrictionTag',
        ),
        migrations.AlterModelTable(
            name='allergytag',
            table='AllergyTags',
        ),
        migrations.AlterModelTable(
            name='ingredienttag',
            table='IngredientTags',
        ),
        migrations.AlterModelTable(
            name='restrictiontag',
            table='RestrictionTag',
        ),
    ]
