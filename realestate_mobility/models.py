from django.db import models

from realestate_app.models import County, State

# Create your models here.


class Mobility(models.Model):

    mobility_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    mobility_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['mobility_id', 'mobility_name']
        verbose_name = 'Mobility_code'

    def __str__(self):
        return self.mobility_id


class MobilityEstimate(models.Model):

    mobility_estimate_value = models.FloatField(blank=True, null=True)
    mobility = models.ForeignKey(
        'Mobility', on_delete=models.CASCADE, related_name='mobility_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_mob', null=True)

    class Meta:
        unique_together = ['mobility', 'county']
        verbose_name = 'Mobility_Estimate'


class MobilityError(models.Model):

    mobility_error_value = models.FloatField(blank=True, null=True)
    mobility = models.ForeignKey(
        'Mobility', on_delete=models.CASCADE, related_name='mobility_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_mob', null=True)

    class Meta:
        unique_together = ['mobility', 'county']
        verbose_name = 'Mobility_Error'


class MobilityStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idtmob', null=True)
    state_total = models.FloatField(blank=True, null=True)
    mobility = models.ForeignKey(
        'Mobility', on_delete=models.CASCADE, related_name='mobility_idtmob', null=True)
    mobility_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'mobility']
        verbose_name = 'Mobility_State_Total'
