from django.db import models

from realestate_app.models import (County, State)

# Create your models here.


class Occupancy(models.Model):

    occupancy_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    occupancy_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['occupancy_id', 'occupancy_name']
        verbose_name = 'Occupancy_code'

    def __str__(self):
        return self.occupancy_id


class OccupancyEstimate(models.Model):

    occupancy_estimate_value = models.FloatField(blank=True, null=True)
    occupancy = models.ForeignKey(
        'Occupancy', on_delete=models.CASCADE, related_name='occupancy_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_occ', null=True)

    class Meta:
        unique_together = ['occupancy', 'county']
        verbose_name = 'Occupancy_Estimate'


class OccupancyError(models.Model):

    occupancy_error_value = models.FloatField(blank=True, null=True)
    occupancy = models.ForeignKey(
        'Occupancy', on_delete=models.CASCADE, related_name='occupancy_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_occ', null=True)

    class Meta:
        unique_together = ['occupancy', 'county']
        verbose_name = 'Occupancy_Error'


class OccupancyStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idtocc', null=True)
    state_total = models.FloatField(blank=True, null=True)
    occupancy = models.ForeignKey(
        'Occupancy', on_delete=models.CASCADE, related_name='occupancy_idtocc', null=True)
    occupancy_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'occupancy']
        verbose_name = 'Occupancy_State_Total'
