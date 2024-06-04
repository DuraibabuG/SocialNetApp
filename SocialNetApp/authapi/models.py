from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    gender = models.CharField(max_length=1, blank=False, default='M')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name
