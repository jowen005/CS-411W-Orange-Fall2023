# Generated by Django 4.2.4 on 2023-09-27 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0004_remove_patron_dietary_restriction_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patron',
            old_name='Patron_taste_tag',
            new_name='patron_taste_tag',
        ),
    ]