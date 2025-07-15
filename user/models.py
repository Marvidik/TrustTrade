from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    language_preference = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    trust_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username
