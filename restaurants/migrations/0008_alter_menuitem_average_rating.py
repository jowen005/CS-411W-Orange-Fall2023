# Generated by Django 4.2.4 on 2023-10-03 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_rename_allergy_tag_allergytag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=3),
        ),
    ]