# Generated by Django 4.0.3 on 2022-05-09 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate_app', '0007_incomeestimate_incomeerror'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaceStateTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_total', models.FloatField(blank=True, null=True)),
                ('race_total', models.FloatField(blank=True, null=True)),
                ('race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='race_idt', to='realestate_app.race')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_idt', to='realestate_app.state')),
            ],
            options={
                'verbose_name': 'Race_State_Total',
                'unique_together': {('state', 'race')},
            },
        ),
    ]
