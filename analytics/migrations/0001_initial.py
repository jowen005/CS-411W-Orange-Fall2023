# Generated by Django 4.2.4 on 2023-11-20 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurants', '0010_menuitem_calorie_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSatisfactionAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_rating', models.DecimalField(decimal_places=2, max_digits=8)),
                ('number_of_rating_total', models.PositiveIntegerField()),
                ('number_of_rating_since', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'AppSatisfactionAnalytics',
            },
        ),
        migrations.CreateModel(
            name='CalorieAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie_level', models.IntegerField(choices=[(0, 'Invalid'), (1, '0 - 199'), (2, '200 - 399'), (3, '400 - 599'), (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'), (7, '1200 - 1399'), (8, '1400 - 1599'), (9, '1600 - 1799'), (10, '1800 - 1999'), (11, '2000 and up')], default=0, null=True)),
                ('number_of_profiles', models.PositiveIntegerField()),
                ('number_of_menuItems', models.PositiveIntegerField()),
                ('number_of_searches', models.PositiveIntegerField()),
                ('number_of_items_added_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Calorie_Analytics',
            },
        ),
        migrations.CreateModel(
            name='GlobalAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_males', models.IntegerField()),
                ('total_females', models.IntegerField()),
                ('total_other', models.IntegerField()),
                ('users_18_24', models.IntegerField()),
                ('users_25_34', models.IntegerField()),
                ('users_35_44', models.IntegerField()),
                ('users_45_54', models.IntegerField()),
                ('users_55_64', models.IntegerField()),
                ('users_65_and_up', models.IntegerField()),
                ('total_users', models.IntegerField()),
                ('total_patrons', models.IntegerField()),
                ('total_restaurants', models.IntegerField()),
                ('total_menu_items', models.IntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Global_Analytics',
            },
        ),
        migrations.CreateModel(
            name='TasteTagAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_patronProfile', models.PositiveIntegerField()),
                ('number_of_menuItem', models.PositiveIntegerField()),
                ('number_of_search', models.PositiveIntegerField()),
                ('number_of_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.tastetag')),
            ],
            options={
                'db_table': 'TasteTagAnalytics',
            },
        ),
        migrations.CreateModel(
            name='RestrictionTagAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_patronProfile', models.PositiveIntegerField()),
                ('number_of_menuItem', models.PositiveIntegerField()),
                ('number_of_search', models.PositiveIntegerField()),
                ('number_of_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restrictiontag')),
            ],
            options={
                'db_table': 'RestrictionTagAnalytics',
            },
        ),
        migrations.CreateModel(
            name='MenuItemPerformanceAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_added_to_bookmark', models.PositiveIntegerField()),
                ('number_of_added_to_History', models.PositiveIntegerField()),
                ('number_of_ratings', models.PositiveIntegerField()),
                ('average_rating', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('menuItem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitem')),
            ],
            options={
                'db_table': 'MenuItemPerformanceAnalytics',
            },
        ),
        migrations.CreateModel(
            name='IngredientTagAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_patronProfile', models.PositiveIntegerField()),
                ('number_of_menuItem', models.PositiveIntegerField()),
                ('number_of_search', models.PositiveIntegerField()),
                ('number_of_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.ingredienttag')),
            ],
            options={
                'db_table': 'IngredientTagAnalytics',
            },
        ),
        migrations.CreateModel(
            name='CookStyleAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_menuItem', models.PositiveIntegerField()),
                ('number_of_search', models.PositiveIntegerField()),
                ('number_of_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.cookstyletag')),
            ],
            options={
                'db_table': 'CookStyleAnalytics',
            },
        ),
        migrations.CreateModel(
            name='AllergiesTagAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_patronProfile', models.PositiveIntegerField()),
                ('number_of_menuItem', models.PositiveIntegerField()),
                ('number_of_search', models.PositiveIntegerField()),
                ('number_of_HIS', models.PositiveIntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.allergytag')),
            ],
            options={
                'db_table': 'AllergiesTagAnalytics',
            },
        ),
    ]
