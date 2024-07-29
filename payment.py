
import stripe
from django.conf import settings
from .models import Transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_charge(amount, currency='usd', description='ASA Transaction', source):
    try:
        charge = stripe.Charge.create(
            amount=int(amount * 100),  # Stripe expects amount in cents
            currency=currency,
            description=description,
            source=source
        )
        return charge
    except stripe.error.StripeError as e:
        # Handle error
        raise e

def release_escrow(transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.escrow and not transaction.completed:
            charge = stripe.Charge.retrieve(transaction.charge_id)
            charge.capture()
            transaction.escrow = False
            transaction.completed = True
            transaction.save()
            return transaction
    except Transaction.DoesNotExist:
        raise ValueError("Transaction not found")
    except stripe.error.StripeError as e:
        # Handle error
        raise e
