from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Wallet, Transaction


class WalletModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')

    def test_create_wallet(self):
        wallet = Wallet.objects.create(user=self.user, balance=100, currency='USD')
        
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.balance, Decimal('100'))
        self.assertEqual(wallet.currency, 'USD')

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.wallet1 = Wallet.objects.create(user=self.user, balance=100, currency='USD')
        self.wallet2 = Wallet.objects.create(user=self.user, balance=50, currency='RUB')

    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            source_wallet=self.wallet1,
            target_wallet=self.wallet2,
            amount=50
        )
        
        self.assertEqual(transaction.source_wallet, self.wallet1)
        self.assertEqual(transaction.target_wallet, self.wallet2)
        self.assertEqual(transaction.amount, Decimal('50'))
        self.assertAlmostEqual(transaction.target_amount, Decimal('4166.50'), places=2)
