# Generated by Django 4.2.4 on 2023-09-27 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0005_rename_patron_taste_tag_patron_patron_taste_tag'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='patron',
            table='PatronProfiles',
        ),
    ]
