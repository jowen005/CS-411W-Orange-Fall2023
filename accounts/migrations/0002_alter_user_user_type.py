# Generated by Django 4.2.4 on 2023-09-03 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('restaurant', 'Restaurant'), ('patron', 'Patron')], max_length=20),
        ),
    ]
