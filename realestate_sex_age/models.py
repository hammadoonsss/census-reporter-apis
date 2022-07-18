from django.db import models

from realestate_app.models import (County, State)

# Create your models here.


class SexAge(models.Model):

    sex_age_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    sex_age_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['sex_age_id', 'sex_age_name']
        verbose_name = "Sex_Age_code"

    def __str__(self):
        return self.sex_age_id


class SexAgeEstimate(models.Model):

    sex_age_estimate_value = models.FloatField(blank=True, null=True)
    sex_age = models.ForeignKey(
        'SexAge', on_delete=models.CASCADE, related_name='sex_age_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_sa', null=True)

    class Meta:
        unique_together = ['sex_age', 'county']
        verbose_name = 'Sex_Age_Estimate'


class SexAgeError(models.Model):

    sex_age_error_value = models.FloatField(blank=True, null=True)
    sex_age = models.ForeignKey(
        'SexAge', on_delete=models.CASCADE, related_name='sex_age_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_sa', null=True)

    class Meta:
        unique_together = ['sex_age', 'county']
        verbose_name = 'Sex_Age_Error'


class SexAgeStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idtsa', null=True)
    state_total = models.FloatField(blank=True, null=True)
    sex_age = models.ForeignKey(
        SexAge, on_delete=models.CASCADE, related_name='sex_age_idtsa', null=True)
    sex_age_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'sex_age']
        verbose_name = 'Sex_Age_State_Total'
