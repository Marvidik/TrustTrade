# wallet/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=12, default=0.00)

    def __str__(self):
        return f"{self.user.email} - Wallet"

    def credit(self, amount):
        self.balance += float(amount)
        self.save()

    def debit(self, amount):
        if self.balance >= float(amount):
            self.balance -= float(amount)
            self.save()
            return True
        return False

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    reference = models.CharField(max_length=100, blank=True, null=True,unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success=models.BooleanField(default=False)
