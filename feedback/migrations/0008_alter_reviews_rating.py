# Generated by Django 4.2.4 on 2023-11-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0007_remove_reviews_menuitem_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.DecimalField(choices=[('0', '0'), ('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5')], decimal_places=2, max_digits=8, null=True),
        ),
    ]