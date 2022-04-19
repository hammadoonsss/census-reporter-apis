# Generated by Django 4.0.3 on 2022-04-18 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate_app', '0002_state_alter_race_options_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaceEstimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_estimate_value', models.FloatField(blank=True, null=True)),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='county_estimate', to='realestate_app.county')),
                ('race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='race_estimate', to='realestate_app.race')),
            ],
            options={
                'verbose_name': 'Race_Estimate',
            },
        ),
        migrations.CreateModel(
            name='RaceError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_error_value', models.FloatField(blank=True, null=True)),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='county_error', to='realestate_app.county')),
                ('race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='race_error', to='realestate_app.race')),
            ],
            options={
                'verbose_name': 'Race_Error',
            },
        ),
    ]
