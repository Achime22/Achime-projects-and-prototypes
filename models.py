
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

class Agreement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_agreements')
    parties = models.ManyToManyField(User, related_name='agreements')
    content = models.TextField()
    audio_file = models.FileField(upload_to='agreements/audio/', null=True, blank=True)
    video_file = models.FileField(upload_to='agreements/video/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    finalized = models.BooleanField(default=False)
    signature = models.JSONField(default=dict)  # To store digital signatures

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Transaction(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    escrow = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mediator_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    transaction_fee = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)  # 1% fee

class Mediator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_active = models.BooleanField(default=True)
