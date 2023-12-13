from django.test import TestCase
from django.contrib.auth import get_user_model
from .serializers import WalletSerializer, TransactionSerializer
from .models import Wallet, Transaction
from decimal import Decimal

class WalletSerializerTest(TestCase):
    def test_serialize_wallet(self):
        user = get_user_model().objects.create(username='testuser')
        wallet_data = {'user': user.id, 'balance': '100.50', 'currency': 'USD'}
        serializer = WalletSerializer(data=wallet_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['user'], user.id)
        self.assertEqual(serialized_data['balance'], '100.50')
        self.assertEqual(serialized_data['currency'], 'USD')

class TransactionSerializerTest(TestCase):
    def test_serialize_transaction(self):
        user = get_user_model().objects.create(username='testuser')
        wallet1 = Wallet.objects.create(user=user, balance=100, currency='USD')
        wallet2 = Wallet.objects.create(user=user, balance=50, currency='RUB')

        data = {
            'source_wallet': wallet1.id,
            'target_wallet': wallet2.id,
            'amount': 50
        }

        serializer = TransactionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        transaction = serializer.save()
        self.assertIsNotNone(transaction)
        self.assertAlmostEqual(transaction.target_amount, Decimal('4166.50'), places=2)

