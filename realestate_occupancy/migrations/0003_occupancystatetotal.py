# Generated by Django 4.0.3 on 2022-06-02 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate_app', '0015_county_occupancy_total'),
        ('realestate_occupancy', '0002_occupancyestimate_occupancyerror'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccupancyStateTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_total', models.FloatField(blank=True, null=True)),
                ('occupancy_total', models.FloatField(blank=True, null=True)),
                ('occupancy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='occupancy_idtocc', to='realestate_occupancy.occupancy')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_idtocc', to='realestate_app.state')),
            ],
            options={
                'verbose_name': 'Occupancy_State_Total',
                'unique_together': {('state', 'occupancy')},
            },
        ),
    ]