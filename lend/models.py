from django.db import models
from user.models import CustomUser
# Create your models here.
class Listing(models.Model):
    LISTING_TYPE_CHOICES = (
        ('lend', 'Lend'),
        ('borrow', 'Borrow'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=LISTING_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_funded = models.BooleanField(default=False)


class Match(models.Model):
    borrower = models.ForeignKey(CustomUser, related_name='borrower_matches', on_delete=models.CASCADE)
    lender = models.ForeignKey(CustomUser, related_name='lender_matches', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
