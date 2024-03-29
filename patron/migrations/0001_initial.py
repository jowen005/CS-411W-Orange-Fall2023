# Generated by Django 4.2.4 on 2023-10-17 22:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0009_alter_menuitem_average_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatronSearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('calorie_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('dietary_restriction', models.CharField(blank=True, max_length=255)),
                ('price_min', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('price_max', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('search_datetime', models.DateTimeField(auto_now_add=True)),
                ('patron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PatronSearchHistory',
            },
        ),
        migrations.CreateModel(
            name='Patron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('calorie_limit', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('price_preference', models.CharField(choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$')], max_length=5)),
                ('zipcode', models.CharField(max_length=10)),
                ('disliked_ingredients', models.ManyToManyField(to='restaurants.ingredienttag')),
                ('patron_allergy_tag', models.ManyToManyField(to='restaurants.allergytag')),
                ('patron_restriction_tag', models.ManyToManyField(to='restaurants.restrictiontag')),
                ('patron_taste_tag', models.ManyToManyField(to='restaurants.tastetag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patron', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PatronProfiles',
            },
        ),
        migrations.CreateModel(
            name='MealHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mealHS_datetime', models.DateTimeField(auto_now_add=True)),
                ('menu_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurants.menuitem')),
                ('patron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MealHistory',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_datetime', models.DateTimeField(auto_now_add=True)),
                ('menu_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitem')),
                ('patron', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Bookmarks',
                'unique_together': {('patron', 'menu_item')},
            },
        ),
    ]
