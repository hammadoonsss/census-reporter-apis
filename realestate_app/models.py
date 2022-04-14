from django.db import models

# Create your models here.


class Race(models.Model):
    race_id = models.CharField(max_length=25, primary_key=True, blank=False, null=False)
    race_name = models.CharField(max_length=225, blank=True, null=True)
    
    class Meta:
        verbose_name = 'race'
    
    def __str__(self):
        return self.race_id
