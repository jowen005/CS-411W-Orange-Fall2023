# Generated by Django 4.2.4 on 2023-10-03 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_alter_menuitem_average_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
    ]
