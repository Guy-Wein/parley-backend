from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    balance = models.FloatField(max_length=10, default=1000)

class Transaction(models.Model):
    card_types = (
        ('credit', 'credit'),
        ('debit', 'debit')
    )
    statuses = (
        ('success', 'success'),
        ('fail', 'fail')
    )
    src_bank_account = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_transactions')
    dst_bank_account = models.ForeignKey('User', on_delete=models.CASCADE, related_name="received_transactions")
    amount = models.FloatField(max_length=10)
    direction = models.CharField(max_length=6, choices=card_types, default='debit')
    status = models.CharField(max_length=7, choices=statuses, default='success')
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.src_bank_account} {self.direction} {self.amount} to {self.dst_bank_account}"

class Advance(models.Model):
    src_bank_account = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_advance')
    dst_bank_account = models.ForeignKey('User', on_delete=models.CASCADE, related_name="received_advance")
    amount = models.FloatField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)
