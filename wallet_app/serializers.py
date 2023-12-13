from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CreateTransactionSerializer(serializers.Serializer):
    source_wallet_id = serializers.IntegerField()
    target_wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    # target_amount = serializers.DecimalField(max_digits=10, decimal_places=2)