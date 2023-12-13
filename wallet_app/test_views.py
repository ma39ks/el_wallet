from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Wallet, Transaction


class WalletListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_wallets(self):
        response = self.client.get('/api/wallets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.count(), 1)
        wallet = Wallet.objects.first()
        self.assertEqual(wallet.user, self.user)

class TransactionListCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.wallet1 = Wallet.objects.create(user=self.user, balance=100, currency='USD')
        self.wallet2 = Wallet.objects.create(user=self.user, balance=50, currency='RUB')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_transaction(self):
        url = reverse('transaction-list-create')
        data = {
            'source_wallet': self.wallet1.id,
            'target_wallet': self.wallet2.id,
            'amount': 50
        }

        # Авторизуем пользователя, чтобы убедиться, что запрос проходит
        self.client.force_login(self.user)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.source_wallet, self.wallet1)
        self.assertEqual(transaction.target_wallet, self.wallet2)
        self.assertEqual(transaction.amount, 50)
        self.assertIsNotNone(transaction.target_amount)


