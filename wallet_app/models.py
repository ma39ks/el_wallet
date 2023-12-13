from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal
from .utils import logger


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('RUB', 'RUB'), ('USD', 'USD')])
    logger.info(f"Wallet created: {user}, {balance}, {currency}")

class Transaction(models.Model):
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='source_transactions')
    target_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='target_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.source_wallet.currency == 'RUB' and self.target_wallet.currency == 'USD':
            exchange_rate = Decimal(0.012)
            self.target_amount = self.amount * exchange_rate
        elif self.source_wallet.currency == 'USD' and self.target_wallet.currency == 'RUB':
            exchange_rate = Decimal(83.33)
            self.target_amount = self.amount * exchange_rate
        logger.info(f"Transaction created: {self.target_amount}")

        super().save(*args, **kwargs)

@receiver(pre_save, sender=Transaction)
def calculate_target_amount(sender, instance, **kwargs):
    if instance.source_wallet.currency == 'RUB' and instance.target_wallet.currency == 'USD':
        exchange_rate = Decimal(0.012)
        instance.target_amount = instance.amount * exchange_rate
    elif instance.source_wallet.currency == 'USD' and instance.target_wallet.currency == 'RUB':
        exchange_rate = Decimal(83.33)
        instance.target_amount = instance.amount * exchange_rate

@receiver(post_save, sender=Transaction)
def update_wallet_balances(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.source_wallet.balance -= instance.amount
        instance.target_wallet.balance += instance.target_amount
        instance.source_wallet.save()
        instance.target_wallet.save()

def get_default_wallet():
    return Wallet.objects.first() or Wallet.objects.create(user=get_user_model().objects.first(), balance=0, currency='RUB')

def lazy():
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    admin_group, _ = Group.objects.get_or_create(name='Admin')
    user_group, _ = Group.objects.get_or_create(name='User')

    wallet_content_type = ContentType.objects.get_for_model(Wallet)
    transaction_content_type = ContentType.objects.get_for_model(Transaction)

    admin_permissions = Permission.objects.filter(content_type__in=[wallet_content_type, transaction_content_type])
    admin_group.permissions.set(admin_permissions)

@receiver(post_save, sender=Wallet)
def log_wallet_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Wallet created: {instance}")

@receiver(post_save, sender=Transaction)
def log_transaction_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Transaction created: {instance}")