# Generated by Django 4.2.4 on 2023-11-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0004_menuitemhistory_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patron',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6),
        ),
    ]
