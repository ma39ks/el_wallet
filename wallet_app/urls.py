from django.urls import path
from .views import WalletListCreateView, WalletDetailView, TransactionListCreateView, TransactionDetailView, index, WalletListView, profile, login_user, login_view, transaction_list, create_transaction, TransactionCreateView
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'login.html'

urlpatterns = [
    path('wallet/', WalletListView.as_view(), name='wallet'),
    path('wallets/', WalletListCreateView.as_view(), name='wallet-list-create'),
    path('wallets/<int:pk>/', WalletDetailView.as_view(), name='wallet-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('', index, name='index'),
    path('login_user', login_user, name='login'),
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('create_transaction/', create_transaction, name='create_transaction'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
