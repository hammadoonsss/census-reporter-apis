from tabnanny import verbose
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
    state_ref_id = models.CharField(max_length=50,blank=True, null=True)

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

    class Meta:
        verbose_name = 'County'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.county_id
