from django import forms
from .models import Transaction


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['target_amount']
        fields = ['source_wallet', 'target_wallet', 'amount']