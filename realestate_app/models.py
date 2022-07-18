
from django.db import models

# Create your models here.


class Race(models.Model):

    race_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    race_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        verbose_name = 'Race_code'

    def __str__(self):
        return self.race_id


class State(models.Model):

    state_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    state_name = models.CharField(max_length=225, blank=True, null=True)
    state_ref_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'State'

    def __str__(self):
        return self.state_id


class County(models.Model):

    county_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    county_name = models.CharField(max_length=225, blank=True, null=True)
    state = models.ForeignKey(
        'State', on_delete=models.CASCADE, related_name='counties', null=True)
    race_total = models.FloatField(blank=True, null=True)
    income_total = models.FloatField(blank=True, null=True)
    poverty_total = models.FloatField(blank=True, null=True)
    education_total = models.FloatField(blank=True, null=True)
    sex_age_total = models.FloatField(blank=True, null=True)
    house_price_total = models.FloatField(blank=True, null=True)
    occupancy_total = models.FloatField(blank=True, null=True)
    mobility_total = models.FloatField(blank=True, null=True)
    tenure_total = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'County'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.county_id


class RaceEstimate(models.Model):

    race_estimate_value = models.FloatField(blank=True, null=True)
    race = models.ForeignKey(
        'Race', on_delete=models.CASCADE, related_name='race_estimate', null=True)
    county = models.ForeignKey(
        'County', on_delete=models.CASCADE, related_name='county_estimate', null=True)

    class Meta:
        unique_together = ['race', 'county']
        verbose_name = 'Race_Estimate'


class RaceError(models.Model):

    race_error_value = models.FloatField(blank=True, null=True)
    race = models.ForeignKey(
        'Race', on_delete=models.CASCADE, related_name='race_error', null=True)
    county = models.ForeignKey(
        'County', on_delete=models.CASCADE, related_name='county_error', null=True)

    class Meta:
        unique_together = ['race', 'county']
        verbose_name = 'Race_Error'


class Income(models.Model):

    income_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    income_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        verbose_name = 'Income_code'

    def __str__(self):
        return self.income_id


class IncomeEstimate(models.Model):

    income_estimate_value = models.FloatField(blank=True, null=True)
    income = models.ForeignKey(
        'Income', on_delete=models.CASCADE, related_name='income_estimate', null=True)
    county = models.ForeignKey(
        'County', on_delete=models.CASCADE, related_name='county_est_in', null=True)

    class Meta:
        unique_together = ['income', 'county']
        verbose_name = 'Income_Estimate'


class IncomeError(models.Model):

    income_error_value = models.FloatField(blank=True, null=True)
    income = models.ForeignKey(
        'Income', on_delete=models.CASCADE, related_name='income_error', null=True)
    county = models.ForeignKey(
        'County', on_delete=models.CASCADE, related_name='county_err_in', null=True)

    class Meta:
        unique_together = ['income', 'county']
        verbose_name = 'Income_Error'


class RaceStateTotal(models.Model):

    state = models.ForeignKey(
        'State', on_delete=models.CASCADE, related_name='state_idt', null=True)
    state_total = models.FloatField(blank=True, null=True)
    race = models.ForeignKey(
        'Race', on_delete=models.CASCADE, related_name='race_idt', null=True)
    race_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'race']
        verbose_name = 'Race_State_Total'


class IncomeStateTotal(models.Model):

    state = models.ForeignKey(
        'State', on_delete=models.CASCADE, related_name='state_idti', null= True)
    state_total = models.FloatField(blank=True, null= True)
    income = models.ForeignKey(
        'Income', on_delete= models.CASCADE, related_name='income_idti', null = True)
    income_total = models.FloatField(blank= True, null= True)

    class Meta:
        unique_together = ['state', 'income']
        verbose_name = 'Income_State_Total'
