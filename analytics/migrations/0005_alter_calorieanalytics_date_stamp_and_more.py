# Generated by Django 4.2.4 on 2023-11-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_allergiestaganalytics_date_stamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calorieanalytics',
            name='date_stamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='menuitemperformanceanalytics',
            name='date_stamp',
            field=models.DateTimeField(),
        ),
    ]
