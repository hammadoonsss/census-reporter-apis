# Generated by Django 4.0.3 on 2022-04-29 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate_app', '0006_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeEstimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_estimate_value', models.FloatField(blank=True, null=True)),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='county_est_in', to='realestate_app.county')),
                ('income', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='income_estimate', to='realestate_app.income')),
            ],
            options={
                'verbose_name': 'Income_Estimate',
                'unique_together': {('income', 'county')},
            },
        ),
        migrations.CreateModel(
            name='IncomeError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_error_value', models.FloatField(blank=True, null=True)),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='county_err_in', to='realestate_app.county')),
                ('income', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='income_error', to='realestate_app.income')),
            ],
            options={
                'verbose_name': 'Income_Error',
                'unique_together': {('income', 'county')},
            },
        ),
    ]
