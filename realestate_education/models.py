
from django.db import models

from realestate_app.models import (State,)

# Create your models here.


class Education(models.Model):

    education_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    education_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['education_id', 'education_name']
        verbose_name = 'Education_code'

    def __str__(self):
        return self.education_id


class EducationEstimate(models.Model):

    education_estimate_value = models.FloatField(blank=True, null=True)
    education = models.ForeignKey(
        'Education', on_delete=models.CASCADE, related_name='education_estimate', null=True)
    county = models.ForeignKey(
        'realestate_app.County', on_delete=models.CASCADE, related_name='county_est_ed', null=True)

    class Meta:
        unique_together = ['education', 'county']
        verbose_name = 'Education_Estimate'


class EducationError(models.Model):

    education_error_value = models.FloatField(blank=True, null=True)
    education = models.ForeignKey(
        'Education', on_delete=models.CASCADE, related_name='education_error', null=True)
    county = models.ForeignKey(
        'realestate_app.County', on_delete=models.CASCADE, related_name='county_err_ed', null=True)

    class Meta:
        unique_together = ['education', 'county']
        verbose_name = 'Education_Error'


class EducationStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idte', null=True)
    state_total = models.FloatField(blank=True, null=True)
    education = models.ForeignKey(
        Education, on_delete=models.CASCADE, related_name='edu_idte', null=True)
    education_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'education']
        verbose_name = 'Education_State_Total'