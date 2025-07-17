from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    language_preference = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    trust_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username

    @property
    def average_trust_score(self):
        from lend.models import TrustRating
        ratings = TrustRating.objects.filter(match__borrower=self)
        if not ratings.exists():
            return None
        return round(sum(r.score for r in ratings) / ratings.count(), 1)


class VerificationDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=50)  # e.g., 'passport', 'national_id'
    front_document = models.ImageField(upload_to='kyc_documents/')
    back_document = models.ImageField(upload_to='kyc_documents/')
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

