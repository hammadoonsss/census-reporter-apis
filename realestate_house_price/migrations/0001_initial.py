# Generated by Django 4.0.3 on 2022-05-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HousePrice',
            fields=[
                ('house_price_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('house_price_name', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'verbose_name': 'House_Price_code',
                'unique_together': {('house_price_id', 'house_price_name')},
            },
        ),
    ]
