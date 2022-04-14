from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email_id = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=25, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'user'
    
    def __str__(self):
        return self.email_id
