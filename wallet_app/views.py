from rest_framework import generics, status
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, CreateTransactionSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.views import LoginView, LogoutView

from django.views.generic import ListView, CreateView
from .models import Wallet, Transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import TransactionForm
from .utils import logger


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/wallet/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def login_user(request):
    return render(request, 'login.html', {})

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'


class TransactionCreateView(PermissionRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transaction_create.html'
    fields = ['source_wallet', 'target_wallet', 'amount']

    permission_required = 'wallet_app.add_transaction'

    def form_valid(self, form):
        return super().form_valid(form)

class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    template_name = 'wallet_list.html'
    context_object_name = 'wallets'
    login_url = 'login'

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'
    login_url = 'login'


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in WalletListCreateView get: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"CreateWallet: {request.data}")
            return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in WalletListCreateView post: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Wallet
    template_name = 'wallet_detail.html'
    context_object_name = 'wallet'
    login_url = 'login'
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in WalletDetailView retrieve: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in WalletDetailView update: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in WalletDetailView destroy: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_current_balance(self, wallet_id):
        wallet = Wallet.objects.get(id=wallet_id)
        return wallet.balance

    def create(self, request, *args, **kwargs):
        adapted_data = {
            'source_wallet_id': request.data.get('source_wallet'),
            'target_wallet_id': request.data.get('target_wallet'),
            'amount': request.data.get('amount'),
            # 'target_amount': request.data.get('target_amount'),
        }

        serializer = self.get_serializer(data=adapted_data)
        serializer.is_valid(raise_exception=True)

        source_wallet = serializer.validated_data['source_wallet']
        target_wallet = serializer.validated_data['target_wallet']
        amount = serializer.validated_data['amount']

        self.perform_create(serializer)

        source_wallet.refresh_from_db()
        target_wallet.refresh_from_db()

        if source_wallet.balance < amount:
            return Response({"error": "Insufficient funds in the source wallet."}, status=status.HTTP_400_BAD_REQUEST)

        source_wallet.balance -= amount
        target_wallet.balance += amount

        source_wallet.save()
        target_wallet.save()

        headers = self.get_success_headers(serializer.data)
        logger.info(f"CreateTransaction: {amount}, {target_wallet.balance}, {source_wallet.balance}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in TransactionListCreateView get: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            adapted_data = {
                'source_wallet_id': request.data.get('source_wallet'),
                'target_wallet_id': request.data.get('target_wallet'),
                'amount': request.data.get('amount'),
                # 'target_amount': request.data.get('target_amount'),
            }
            serializer = CreateTransactionSerializer(data=adapted_data)
            serializer.is_valid(raise_exception=True)

            source_wallet_id = serializer.validated_data['source_wallet_id']
            current_balance = self.get_current_balance(source_wallet_id)
            logger.info(f"CreateTransaction: {source_wallet_id}, {current_balance}")
            return Response({"current_balance": current_balance}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"An error occurred in TransactionListCreateView post: {e}, {serializer}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionDetailView(generics.RetrieveAPIView):
    model = Transaction
    template_name = 'transaction_detail.html'
    context_object_name = 'transaction'
    login_url = 'login'
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in TransactionDetailView retrieve: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    return render(request, 'index.html')

# @login_required
# def profile(request):
#     return render(request, 'profile.html')

@login_required
def profile(request):
    return render(request, 'wallet_app/profile.html')