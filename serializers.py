
from rest_framework import serializers
from .models import Agreement, Wallet, Transaction, Mediator

class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class MediatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mediator
        fields = '__all__'
