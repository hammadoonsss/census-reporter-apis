from django.db import models

from realestate_app.models import (County, State)

# Create your models here.


class HousePrice(models.Model):

    house_price_id = models.CharField(
        max_length=25, primary_key=True, blank=False, null=False)
    house_price_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        unique_together = ['house_price_id', 'house_price_name']
        verbose_name = 'House_Price_code'

    def __str__(self):
        return self.house_price_id


class HousePriceEstimate(models.Model):

    house_price_estimate_value = models.FloatField(blank=True, null=True)
    house_price = models.ForeignKey(
        'HousePrice', on_delete=models.CASCADE, related_name='house_price_estimate', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_est_hp', null=True)

    class Meta:
        unique_together = ['house_price', 'county']
        verbose_name = 'House_Price_Estimate'


class HousePriceError(models.Model):

    house_price_error_value = models.FloatField(blank=True, null=True)
    house_price = models.ForeignKey(
        'HousePrice', on_delete=models.CASCADE, related_name='house_price_error', null=True)
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name='county_err_hp', null=True)

    class Meta:
        unique_together = ['house_price', 'county']
        verbose_name = 'House_Price_Error'


class HousePriceStateTotal(models.Model):

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_idthp', null=True)
    state_total = models.FloatField(blank=True, null=True)
    house_price = models.ForeignKey(
        HousePrice, on_delete=models.CASCADE, related_name='hp_idthp', null=True)
    house_price_total = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['state', 'house_price']
        verbose_name = 'House_Price_State_Total'
