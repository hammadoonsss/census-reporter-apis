from django.db import models
from realestate_app.models import County, State
# Create your models here.


class Poverty(models.Model):

    poverty_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    poverty_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['poverty_id', 'poverty_name']
        verbose_name = 'Poverty_code'

    def __str__(self):
        return self.poverty_id


class PovertyEstimate(models.Model):

    poverty_estimate_value = models.FloatField(blank=True, null=True)
    poverty = models.ForeignKey(
        'Poverty', on_delete=models.CASCADE, related_name='poverty_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_pov', null=True)

    class Meta:
        unique_together = ['poverty', 'county']
        verbose_name = 'Poverty_estimate'


class PovertyError(models.Model):

    poverty_error_value = models.FloatField(blank=True, null=True)
    poverty = models.ForeignKey(
        'Poverty', on_delete=models.CASCADE, related_name='poverty_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_pov', null=True)

    class Meta:
        unique_together = ['poverty', 'county']
        verbose_name = 'Poverty_error'

class PovertyStateTotal(models.Model):

    poverty_total = models.FloatField(blank=True, null=True)
    state_total = models.FloatField(blank=True, null=True)
    poverty = models.ForeignKey(
        'Poverty', on_delete= models.CASCADE, related_name="poverty_pst_id", null=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="state_pst_id", null=True)

    class Meta:

        unique_together = ['poverty', 'state']
        verbose_name = 'Poverty_State'
