# Generated by Django 4.2.4 on 2023-08-31 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('price_level', models.PositiveSmallIntegerField(choices=[(1, '$'), (2, '$$'), (3, '$$$')])),
                ('phone_number', models.CharField(max_length=12)),
                ('website', models.URLField()),
                ('street_name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='RestTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'RestTags',
            },
        ),
        migrations.CreateModel(
            name='RestaurantOpenHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mon_open', models.TimeField()),
                ('mon_close', models.TimeField()),
                ('tue_open', models.TimeField()),
                ('tue_close', models.TimeField()),
                ('wed_open', models.TimeField()),
                ('wed_close', models.TimeField()),
                ('thu_open', models.TimeField()),
                ('thu_close', models.TimeField()),
                ('fri_open', models.TimeField()),
                ('fri_close', models.TimeField()),
                ('sat_open', models.TimeField()),
                ('sat_close', models.TimeField()),
                ('sun_open', models.TimeField()),
                ('sun_close', models.TimeField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
            options={
                'db_table': 'RestOpenHours',
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tags',
            field=models.ManyToManyField(to='restaurants.resttag'),
        ),
    ]
