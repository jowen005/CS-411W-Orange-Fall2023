# Generated by Django 4.2.4 on 2023-11-16 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0009_alter_menuitem_average_rating'),
        ('feedback', '0009_alter_reviews_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSatisfaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=255, null=True)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('review_datetime', models.DateTimeField(auto_now_add=True)),
                ('patron', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurants.restaurant')),
            ],
        ),
    ]
