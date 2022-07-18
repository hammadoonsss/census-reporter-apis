from django.db import models

from realestate_app.models import (County, State)

# Create your models here.


class Tenure(models.Model):

    tenure_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    tenure_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['tenure_id', 'tenure_name']
        verbose_name = "Tenure_code"

    def __str__(self):
        return self.tenure_id


class TenureEstimate(models.Model):

    tenure_estimate_value = models.FloatField(blank=True, null=True)
    tenure = models.ForeignKey(
        'Tenure', on_delete=models.CASCADE, related_name='tenure_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_te', null=True)

    class Meta:
        unique_together = ['tenure', 'county']
        verbose_name = 'Tenure_Estimate'


class TenureError(models.Model):

    tenure_error_value = models.FloatField(blank=True, null=True)
    tenure = models.ForeignKey(
        'Tenure', on_delete=models.CASCADE, related_name='tenure_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_te', null=True)

    class Meta:
        unique_together = ['tenure', 'county']
        verbose_name = 'Tenure_Error'


class TenureStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idtte', null=True)
    state_total = models.FloatField(blank=True, null=True)
    tenure = models.ForeignKey(
        Tenure, on_delete=models.CASCADE, related_name='tenure_idtte', null=True)
    tenure_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'tenure']
        verbose_name = 'tenure_State_Total'
